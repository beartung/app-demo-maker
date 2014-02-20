package com.demo.maker;

import android.app.Activity;
import android.app.AlertDialog;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;

import android.os.AsyncTask;
import android.os.Bundle;

import android.util.Log;

import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;

import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.demo.maker.DemoApp;
import com.demo.maker.api.Api;
import com.demo.maker.model.Env;
import com.demo.maker.model.Store;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import com.nostra13.universalimageloader.core.ImageLoader;

import java.util.ArrayList;

import org.json.JSONObject;

public class Demo extends Activity implements View.OnClickListener, AdapterView.OnItemClickListener {

    private static final String TAG = "DEMO";

    private GridView grid;
    private GridAdapter adapter;

    private View line;
    private Animation anim;
    private Button qrcodeButton;
    private LoadTask task; 
    private ArrayList<Env> apps;
    private String ids;
    private String server;
    private Store store;

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        store = Store.get(this);

        line = (View)findViewById(R.id.line);
        anim = AnimationUtils.loadAnimation(this, R.anim.loading);

        qrcodeButton = (Button)findViewById(R.id.btn);
        qrcodeButton.setOnClickListener(this);

        try{
            PackageManager pm = getPackageManager();
            PackageInfo packageInfo = pm.getPackageInfo(getPackageName(), 0);
            String versionName = packageInfo.versionName;
            qrcodeButton.setText(getString(R.string.slogan, versionName));
        }catch (Exception e){
        }

        apps = new ArrayList<Env>();
        ids = store.getString("app_ids", "");
        if (ids.length() > 0){
            String [] ss = ids.split(":");
            for (String s : ss){
                JSONObject a = store.getJSON(s);
                if (a != null){
                    apps.add(new Env(a));
                }
            }
        }

        server = store.getString("api_host", Api.HOST);
        adapter = new GridAdapter();

        grid = (GridView)findViewById(R.id.grid);
        grid.setAdapter(adapter);
        grid.setOnItemClickListener(this);

    }

    @Override
    public void onDestroy(){
        super.onDestroy();
        if (task != null) task.cancel(true);
    }

    @Override
    public void onClick(View view){
        Log.d(TAG, "start scan"); 
        IntentIntegrator.initiateScan(this, "QR_CODE", getString(R.string.prompt));
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id){
        Env app = (Env)apps.get(position);
        if (app != null && app.pageIds.length > 0){
            Log.d(TAG, "click url " + app.api); 
            task = new LoadTask(app.api);
            task.execute();
        }
    }

    public boolean onCreateOptionsMenu(Menu menu){
        //getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    public boolean onOptionsItemSelected (MenuItem item){
        int id = item.getItemId();
        switch (id){
            case R.id.setting:
                final EditText edit = new EditText(this);
                server = store.getString("api_host", Api.HOST);
                edit.setText(server);
                edit.setSelection(server.length());
                AlertDialog d = new AlertDialog.Builder(this)
                                .setTitle(R.string.setting_title)
                                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                                    @Override
                                    public void onClick(DialogInterface dialogInterface, int i) {
                                        store.saveString("api_host", edit.getText().toString().trim());
                                    }
                                })
                                .setView(edit)
                                .create();
                d.show();
                break;
            case android.R.id.home:
                finish();
                break;
        }
        return true;
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        Log.d(TAG, "start done"); 
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        if (scanResult != null) {
            // handle scan result
            String url = scanResult.getContents();
            Log.d(TAG, "scan url = " + url);
            if (url != null){
                task = new LoadTask(url);
                task.execute();
            }
        }
    }

    private class GridAdapter extends BaseAdapter {

        public int getCount() {
            return apps.size();
        }

        public View getView(int position, View convertView, ViewGroup parent){
            ViewHolder h = null;
            if (convertView == null) {
                convertView = getLayoutInflater().inflate(R.layout.item_app, null);
                h = new ViewHolder();
                h.icon = (ImageView)convertView.findViewById(R.id.icon);
                h.name = (TextView)convertView.findViewById(R.id.name);
                convertView.setTag(h);
            }else{
                h = (ViewHolder) convertView.getTag();
            }
            Env app = (Env)getItem(position);
            if (app != null){
                h.name.setText(app.name);
                ImageLoader.getInstance().displayImage(app.icon, h.icon);
            }
            return convertView;
        }

        public long getItemId(int position) {
            return 0;
        }

        public Object getItem(int position) {
            return apps.get(position);
        }

    }

    private static class ViewHolder {
        ImageView icon;
        TextView name;
    };

    private class LoadTask extends AsyncTask<Void, Void, Integer> {

        private String url;
        private Env env;

        public LoadTask(String url){
            this.url = url;
        }

        protected void onPreExecute() {
            line.startAnimation(anim);
        }

        protected Integer doInBackground(Void... p) {
            try {
                Api api = new Api(getApplicationContext());
                server = store.getString("api_host", Api.HOST);
                api.setApiHost(server);
                JSONObject json = api.get(url);
                if (json != null){
                    Log.d(TAG, "json " + json.toString());
                    env = new Env(json);
                    if (!store.contains(env.id)){
                        ids = ids + ":" + env.id;
                        store.saveString("app_ids", ids);
                        apps.add(env);
                    }
                    store.saveJSON(env.id, json);
                    Log.d(TAG, "apps size " + apps.size());
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return 0;
        }

        protected void onPostExecute(Integer ret) {
            line.clearAnimation();
            if (adapter != null){
                Log.d(TAG, "adapter count " + adapter.getCount());
                adapter.notifyDataSetChanged();
                Toast.makeText(Demo.this, R.string.start, Toast.LENGTH_SHORT).show();
                if (env != null && env.pageIds.length > 0){
                    DemoApp.startPage(Demo.this, env, env.pageIds[0]);
                }
            } 
        }

    } 

}

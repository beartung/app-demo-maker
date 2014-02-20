package com.demo.maker;

import android.app.Activity;

import android.content.Intent;

import android.os.AsyncTask;
import android.os.Bundle;

import android.util.Log;

import android.view.View;
import android.view.ViewGroup;

import android.widget.AbsoluteLayout.LayoutParams;
import android.widget.AbsoluteLayout;
import android.widget.Button;
import android.widget.ImageView;

import com.demo.maker.model.Env;

import com.nostra13.universalimageloader.core.ImageLoader;

import java.util.ArrayList;

import org.json.JSONObject;

public class Page extends Activity implements View.OnClickListener {

    private static final String TAG = "PAGE";

    private Env env;
    private Env.Page page;
    private String id;
    private String refer;

    private AbsoluteLayout root;

    @Override
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.page);

        root = (AbsoluteLayout)findViewById(R.id.root);

        onHandleIntent(getIntent(), false);
    }

    @Override
    public void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        onHandleIntent(intent, true);
    }

    private void onHandleIntent(Intent intent, boolean fromNewIntent) {
        Log.d(TAG, "onHandleIntent " + fromNewIntent);
        try{
            id = intent.getStringExtra("id");
            Log.d(TAG, "id " + id);
            refer = intent.getStringExtra("refer");
            Log.d(TAG, "refer " + refer);
            env = new Env(new JSONObject(intent.getStringExtra("env")));
            Log.d(TAG, "env " + env.toString());
            page = env.getPage(id);
            buildPage(env, page);
        }catch (Exception e){
        
        }
    }

    private void buildPage(Env env, Env.Page page){
        ImageView img = (ImageView)findViewById(R.id.img);
        img.setLayoutParams(new LayoutParams(page.width, page.height, page.x, page.y));
        ImageLoader.getInstance().displayImage(page.photo, img);
        for (Env.Action a : page.actions){
            Button b = new Button(this);
            b.setBackgroundResource(R.drawable.bg_action);
            LayoutParams p = new LayoutParams(a.width, a.height, a.x, a.y);
            root.addView(b, p);
            b.setTag(a);
            if (Env.ACTION_TYPE_TOUCH.equals(a.type)){
                b.setOnClickListener(this);
            }
        }
    }

    @Override
    public void onDestroy(){
        super.onDestroy();
    }

    @Override
    public void onClick(View view){
        Log.d(TAG, "onClick"); 
        Env.Action a = (Env.Action)view.getTag();
        if (a != null){
            try{
                if (a.dismiss || a.toPageId.equals(refer)){
                    finish();
                }else{
                    DemoApp.startPage(this, env, a.fromPageId, a.toPageId);
                }
            }catch (Exception e){
            }
        }
    }

}

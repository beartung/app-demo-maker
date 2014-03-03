package com.demo.maker;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;

import android.content.Intent;

import android.os.AsyncTask;
import android.os.Bundle;

import android.util.Log;

import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;

import android.widget.AbsoluteLayout.LayoutParams;
import android.widget.AbsoluteLayout;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import com.demo.maker.model.Env;

import com.nostra13.universalimageloader.core.ImageLoader;

import java.util.ArrayList;

import org.json.JSONObject;

public class Runner extends Activity implements View.OnClickListener, View.OnTouchListener {


    private static final String TAG = "RUNNER";
    private static final int MIN_DISTANCE = 100;
    private float downX, downY, upX, upY;

    private Env env;
    private String rootId;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try{
            Intent intent = getIntent();
            rootId = intent.getStringExtra("id");
            Log.d(TAG, "id " + rootId);
            String refer = intent.getStringExtra("refer");
            Log.d(TAG, "refer " + refer);
            env = new Env(new JSONObject(intent.getStringExtra("env")));
            Log.d(TAG, "env " + env.toString());
            PageFragment pf = new PageFragment();
            pf.env = env;
            pf.id = rootId;
            pf.refer = refer;
            getFragmentManager().beginTransaction()
                .add(android.R.id.content, pf, rootId)
                .addToBackStack(null)
                .commit();
        }catch (Exception e){
        
        }
    }

    public static class PageFragment extends Fragment {

        Env env;
        String id;
        String refer;

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
            Env.Page page = env.getPage(id);
            AbsoluteLayout root = (AbsoluteLayout)inflater.inflate(page.isSubpage() ? R.layout.sub_page : R.layout.page,
                                    container, false);
            AbsoluteLayout sub = null;

            if (page.isSubpage()){
                sub = (AbsoluteLayout)root.findViewById(R.id.sub);
                sub.setLayoutParams(new LayoutParams(page.width, page.height, page.x, page.y));
            }

            ImageView img = (ImageView)root.findViewById(R.id.img);
            if (page.isSubpage()){
                img.setLayoutParams(new LayoutParams(page.width, page.height, 0, 0));
            }else{
                img.setLayoutParams(new LayoutParams(page.width, page.height, page.x, page.y));
            }
            if (page.photo.length() > 0){
                ImageLoader.getInstance().displayImage(page.photo, img);
            }else{
                img.setBackgroundColor(getResources().getColor(R.color.bg_img));
            }

            for (String pid : page.subpageIds){
                Env.Page p = env.getPage(pid);
                Log.d(TAG, "page id=" + p.id + " type=" + p.type);
                if (p.type.equals(Env.PAGE_TYPE_LIST)){
                    ListView l = new ListView(getActivity());
                    LayoutParams lp = new LayoutParams(p.width, p.height, p.x, p.y);
                    l.setBackgroundColor(getResources().getColor(R.color.bg_list));
                    ListAdapter adapter = new ListAdapter(env, p, getActivity());
                    if (page.isSubpage()){
                        sub.addView(l, lp);
                    }else{
                        root.addView(l, lp);
                    }
                    l.setAdapter(adapter);
                }
            }

            for (Env.Action a : page.actions){
                View v;
                Log.d(TAG, "action type= " + a.type);
                if (a.type.equals(Env.ACTION_TYPE_INPUT)){
                    Log.d(TAG, "EditView");
                    EditText e = (EditText)inflater.inflate(R.layout.view_edit, null, false);
                    v = e;
                }else{
                    Log.d(TAG, "Button");
                    Button b = new Button(getActivity());
                    b.setBackgroundResource(R.drawable.bg_action);
                    v = b;
                }
                LayoutParams p = new LayoutParams(a.width, a.height, a.x, a.y);
                v.setTag(a);
                if (page.isSubpage()){
                    sub.addView(v, p);
                }else{
                    root.addView(v, p);
                }
                if (Env.ACTION_TYPE_TOUCH.equals(a.type) || Env.ACTION_TYPE_BACK.equals(a.type)){
                    v.setOnClickListener((View.OnClickListener)getActivity());
                }else if (Env.ACTION_TYPE_SLIDE.contains(a.type)){
                    v.setOnTouchListener((View.OnTouchListener)getActivity());
                }
            }
            return root;
        }

    };

    public boolean onTouch(View v, MotionEvent event){
        switch(event.getAction()){
                case MotionEvent.ACTION_DOWN:
                    downX = event.getX();
                    downY = event.getY();
                    return true;

                case MotionEvent.ACTION_UP:
                    upX = event.getX();
                    upY = event.getY();

                    float deltaX = downX - upX;
                    float deltaY = downY - upY;

                    // swipe horizontal?
                    if(Math.abs(deltaX) > MIN_DISTANCE){
                        // left or right
                        if(deltaX < 0) { onLeftToRightSwipe(v); return true; }
                        if(deltaX > 0) { onRightToLeftSwipe(v); return true; }
                    } else {
                        // swipe vertical?
                        if(Math.abs(deltaY) > MIN_DISTANCE){
                            // top or down
                            if(deltaY < 0) { onTopToBottomSwipe(v); return true; }
                            if(deltaY > 0) { onBottomToTopSwipe(v); return true; }
                        } else {
                            return false; // We don't consume the event
                        }
                   }
        }
        return false;
    }

    @Override
    public void onClick(View view){
        Log.d(TAG, "onClick"); 
        Env.Action a = (Env.Action)view.getTag();
        Log.d(TAG, "tag " + a); 
        if (Env.ACTION_TYPE_BACK.equals(a.type)){
            FragmentManager m = getFragmentManager();
            PageFragment f = (PageFragment)m.findFragmentByTag(a.fromPageId);
            if (a.fromPageId.equals(rootId)){
                finish();
            }else{
                Log.d(TAG, "detach " + f.id);
                m.beginTransaction().detach(f).commit();
            }
        }else{
            doAction(a);
        }
    }

    private void doAction(Env.Action a){
        if (a != null){
            FragmentManager m = getFragmentManager();
            Env.Page p = env.getPage(a.fromPageId);
            String fromPageId = a.fromPageId;
            if (p.type.equals(Env.PAGE_TYPE_ITEM)){
                fromPageId = (env.getPage(p.parentId)).parentId;
            }
            PageFragment f = (PageFragment)m.findFragmentByTag(fromPageId);
            try{
                if (a.dismiss || a.toPageId.equals(f.refer)){
                    if (a.fromPageId.equals(rootId) && a.toPageId.equals("0")){
                        finish();
                    }else{
                        Log.d(TAG, "detach " + f.id);
                        rootId = a.toPageId;
                        m.popBackStackImmediate();
                        m.beginTransaction().detach(f).commit();
                    }
                }
                f = (PageFragment)m.findFragmentByTag(a.toPageId);
                FragmentTransaction ft;
                if (f == null){
                    f = new PageFragment();
                    f.env = env;
                    f.id = a.toPageId;
                    f.refer = a.fromPageId;
                    Log.d(TAG, "add " + f.id);
                    ft = m.beginTransaction();

                    int in = 0;
                    int out = 0;
                    if (Env.ACTION_TYPE_SLIDE.contains(a.type)){
                        if (a.type.equals(Env.ACTION_TYPE_SLIDE_LEFT)){
                            in = R.anim.slide_in_left;
                            out = R.anim.slide_out_right;
                        }else if (a.type.equals(Env.ACTION_TYPE_SLIDE_RIGHT)){
                            in = R.anim.slide_in_right;
                            out = R.anim.slide_out_left;
                        }else if (a.type.equals(Env.ACTION_TYPE_SLIDE_UP)){
                            in = R.anim.slide_in_up;
                            out = R.anim.slide_out_down;
                        }else if (a.type.equals(Env.ACTION_TYPE_SLIDE_DOWN)){
                            in = R.anim.slide_in_down;
                            out = R.anim.slide_out_up;
                        }

                        Log.d(TAG, "use CustomAnimations " + f.id);
                        ft.setCustomAnimations(in, 0, 0, out);
                    }

                    ft.add(android.R.id.content, f, f.id).addToBackStack(null);
                }else{
                    Log.d(TAG, "attach " + f.id);
                    ft = m.beginTransaction().attach(f);
                }
                ft.commit();
            }catch (Exception e){
                e.printStackTrace();
            }
        }
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        int c = getFragmentManager().getBackStackEntryCount();
        Log.d(TAG, "onBackPressed " + c);
        if (c == 0){
            finish();
        }
    }

    @Override
    public void onDestroy(){
        super.onDestroy();
    }

    public void onRightToLeftSwipe(View v){
        Log.i(TAG, "RightToLeftSwipe!");
        Env.Action a = (Env.Action)v.getTag();
        Log.d(TAG, "tag " + a); 
        if (a != null && a.type.equals(Env.ACTION_TYPE_SLIDE_LEFT)){
            doAction(a);
        } 
    }

    public void onLeftToRightSwipe(View v){
        Log.i(TAG, "LeftToRightSwipe!");
        Env.Action a = (Env.Action)v.getTag();
        Log.d(TAG, "tag " + a); 
        if (a != null && a.type.equals(Env.ACTION_TYPE_SLIDE_RIGHT)){
            doAction(a);
        } 
    }

    public void onTopToBottomSwipe(View v){
        Log.i(TAG, "onTopToBottomSwipe!");
        Env.Action a = (Env.Action)v.getTag();
        Log.d(TAG, "tag " + a); 
        if (a != null && a.type.equals(Env.ACTION_TYPE_SLIDE_DOWN)){
            doAction(a);
        } 
    }

    public void onBottomToTopSwipe(View v){
        Log.i(TAG, "onBottomToTopSwipe!");
        Env.Action a = (Env.Action)v.getTag();
        Log.d(TAG, "tag " + a); 
        if (a != null && a.type.equals(Env.ACTION_TYPE_SLIDE_UP)){
            doAction(a);
        } 
    }

    private static class ListAdapter extends BaseAdapter{

        private Env env;
        private Env.Page list;
        private Activity act;

        public ListAdapter(Env e, Env.Page p, Activity r){
            env = e;
            list = p;
            act = r;
        }

        public int getCount() {
            return 30;
        }

        public Object getItem(int position) {
            try {
                return env.getPage(list.subpageIds[position % list.subpageIds.length]);
            } catch (Exception e) {
                return null;
            }
        }

        public long getItemId(int position) {
            return position;
        }

        public View getView(int position, View convertView, ViewGroup parent) {
            Log.d(TAG, "getView " + position);
            Env.Page page = (Env.Page)getItem(position);
            AbsoluteLayout root = (AbsoluteLayout)LayoutInflater.from(act).inflate(R.layout.item_page, null, false);
            ImageView img = (ImageView)root.findViewById(R.id.img);
            if (page.photo.length() > 0){
                ImageLoader.getInstance().displayImage(page.photo, img);
            }else{
                img.setBackgroundColor(act.getResources().getColor(R.color.bg_img));
            }
            for (Env.Action a : page.actions){
                View v;
                Log.d(TAG, "action type= " + a.type);
                if (a.type.equals(Env.ACTION_TYPE_INPUT)){
                    Log.d(TAG, "EditView");
                    EditText e = (EditText)LayoutInflater.from(act).inflate(R.layout.view_edit, null, false);
                    v = e;
                }else{
                    Log.d(TAG, "Button");
                    Button b = new Button(act);
                    b.setBackgroundResource(R.drawable.bg_action);
                    v = b;
                }
                LayoutParams p = new LayoutParams(a.width, a.height, a.x, a.y);
                v.setTag(a);
                root.addView(v, p);
                if (Env.ACTION_TYPE_TOUCH.equals(a.type) || Env.ACTION_TYPE_BACK.equals(a.type)){
                    v.setOnClickListener((View.OnClickListener)act);
                }else if (Env.ACTION_TYPE_SLIDE.contains(a.type)){
                    v.setOnTouchListener((View.OnTouchListener)act);
                }
            }
            convertView = root;
            return convertView;
        }

    }
}

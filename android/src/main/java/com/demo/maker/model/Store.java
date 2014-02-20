package com.demo.maker.model;
import android.content.Context;
import android.content.SharedPreferences;

import android.util.Log;

import org.json.JSONObject;

public class Store{

    private SharedPreferences pref;
    private final String TAG = "Store";

    private static Store _store = null;

    public static Store get(Context ctx){
        if (_store == null){
            _store = new Store(ctx.getApplicationContext());
        }
        return _store;
    }

    private Store(Context ctx){
        pref = ctx.getSharedPreferences("demo", 0);
    }

    public JSONObject getJSON(String name){
        JSONObject r = null;
        try {
            String s = pref.getString(name, null);
            //Log.d(TAG, "getJSON name=" + name + " : " + s);
            r = new JSONObject(s);
        }catch (Exception e){
            e.printStackTrace(); 
        }
        return r;
    }

    public void saveJSON(String name, JSONObject value){
        if (name != null && name.length() > 0 && value != null){
            //Log.d(TAG, "saveJSON name=" + name + " : " + value.toString());
            pref.edit().putString(name, value.toString()).apply();
        }
    }

    public String getString(String name){
        return pref.getString(name, null);
    }

    public String getString(String name, String defaultValue){
        String s = pref.getString(name, defaultValue);
        //Log.d(TAG, "getString name=" + name + " : " + s);
        return s;
    }

    public void saveString(String name, String value){
        if (name != null && name.length() > 0 && value != null){
            //Log.d(TAG, "saveString name=" + name + " : " + value);
            pref.edit().putString(name, value).apply();
        }
    }

    public boolean contains(String name){
        return pref.contains(name);
    }

    public void removeKey(String name){
        pref.edit().remove(name).apply(); 
    }

}

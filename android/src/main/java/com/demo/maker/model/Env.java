package com.demo.maker.model;

import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;

public class Env {

    public static final String ACTION_TYPE_TOUCH       = "T";
    public static final String ACTION_TYPE_SLIDE       = "LRUD";
    public static final String ACTION_TYPE_SLIDE_LEFT  = "L";
    public static final String ACTION_TYPE_SLIDE_RIGHT = "R";
    public static final String ACTION_TYPE_SLIDE_UP    = "U";
    public static final String ACTION_TYPE_SLIDE_DOWN  = "D";
    public static final String ACTION_TYPE_BACK        = "B";
    public static final String ACTION_TYPE_INPUT       = "I";
    public static final String ACTION_TYPE_GALLERY     = "G";
    public static final String ACTION_TYPE_CAMERA      = "C";
    public static final String ACTION_TYPE_SHARE       = "S";


    public static final String PAGE_TYPE_NORMAL        = "N";
    public static final String PAGE_TYPE_LIST          = "L";
    public static final String PAGE_TYPE_PAGER         = "P";
    public static final String PAGE_TYPE_ITEM          = "I";
    public static final String PAGE_TYPE_DIALOG        = "D";

    public class Action {

        public String type;
        public int x;
        public int y;
        public int width;
        public int height;
        public String fromPageId;
        public String toPageId;
        public boolean dismiss;

        public Action(JSONObject json){
            x = json.optInt("x", 0); 
            y = json.optInt("y", 0); 
            width = json.optInt("width", 0); 
            height = json.optInt("height", 0); 
            fromPageId = json.optString("page_id");
            toPageId = json.optString("to_page_id");
            type = json.optString("type");
            dismiss = json.optBoolean("dismiss", false);
        }

    }

    public class Page {

        public String id;
        public String name;
        public String parentId;
        public int x;
        public int y;
        public int width;
        public int height;
        public String photo;
        public String type;
        public String[] subpageIds;

        public Action[] actions;

        public boolean isSubpage(){
            return !parentId.equals("0");
        }

        public Page(JSONObject json){
            id = json.optString("id");
            name = json.optString("name");
            parentId = json.optString("parent_id");
            photo = json.optString("photo");
            type = json.optString("type");
            x = json.optInt("x", 0); 
            y = json.optInt("y", 0); 
            width = json.optInt("width", 0); 
            height = json.optInt("height", 0); 
            
            JSONArray as = json.optJSONArray("actions");
            if (as != null){
                actions = new Action[as.length()];
                for (int i = 0; i < as.length(); i++){
                    actions[i] = new Action(as.optJSONObject(i));
                }
            }
            JSONArray sp = json.optJSONArray("sub_page_ids");
            if (sp != null){
                subpageIds = new String[sp.length()];
                for (int i = 0; i < sp.length(); i++){
                    subpageIds[i] = sp.optString(i);
                }
            }
        }

    }
        
    public JSONObject data;

    public String id;
    public String icon;
    public String name;
    public String api;
    public String[] pageIds;
    public HashMap<String, Page> pages;
        
    public Env(JSONObject json){
        data = json;
        try{
            id = json.optString("id");
            icon = json.optString("icon");
            name = json.optString("name");
            api = json.optString("api");

            JSONArray is = json.optJSONArray("page_ids");
            JSONObject ps = json.optJSONObject("pages");
            if (is != null){
                pageIds = new String[is.length()];
                pages = new HashMap<String, Page>();
                
                for (int i = 0; i < is.length(); i++){
                    pageIds[i] = is.optString(i);
                    pages.put(pageIds[i], new Page(ps.optJSONObject(pageIds[i])));
                }
            }
        }catch (Exception e){

        }
    }

    public Page getPage(String id){
        return pages.get(id);
    }

    public String toString(){
        return data.toString();
    }

}

package com.api;

import org.json.JSONException;
import org.json.JSONObject;

public class ApiError extends Exception{

    public JSONObject json;
    public int status;
    public String msg;

    public ApiError(final int status, final String r){
        this.status = status;
        try{
            json = new JSONObject(r);
            msg = json.optString("message", "");
        }catch (JSONException e){
            json = null;
            msg = "解析失败，请检查服务器地址是否正确。";
            e.printStackTrace(); 
        } 
    }

    public String toString(){
        return "[ApiError status=" + status + ", msg=" + msg + "]";
    }

}

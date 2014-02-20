package com.demo.maker.api;

import android.content.Context;

import com.api.ApiBase;
import com.api.ApiError;
import com.api.http.RequestParams;

public class Api extends ApiBase {

    public static final String HOST = "m.dapps.douban.com";

    public Api(Context context){
        super(context);
        setApiHost(host);
        addHeader("Accept", "application/json");
    }

}

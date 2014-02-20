package com.api;

import android.content.Context;
import android.content.Intent;

import android.util.Log;

import java.io.IOException;

import java.net.URI;

import java.util.HashMap;
import java.util.Map;

import com.api.http.HttpClientUtils;
import com.api.http.RequestParams;

import org.apache.http.*;
import org.apache.http.client.HttpClient;
import org.apache.http.client.RedirectHandler;
import org.apache.http.client.methods.*;
import org.apache.http.client.params.ClientPNames;
import org.apache.http.entity.BufferedHttpEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.DefaultRedirectHandler;
import org.apache.http.impl.client.EntityEnclosingRequestWrapper;
import org.apache.http.impl.client.RequestWrapper;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ApiBase{

    protected static final String TAG = "Api";
    protected static final String VERSION = "1.0";
    protected static final String API_HOST = "api.xx.com";

    protected String host = API_HOST;
    protected HttpClient client;
    protected Context context;
    protected final Map<String, String> clientHeaderMap;

    public ApiBase(Context context){
        this.context = context;  
        this.client = HttpClientUtils.getHttpClient();
        HttpClientUtils.setUserAgent(this.client, String.format("android-api/%s", VERSION));
        if (this.client instanceof DefaultHttpClient){
            DefaultHttpClient dc = (DefaultHttpClient)this.client;
            dc.getParams().setParameter(ClientPNames.ALLOW_CIRCULAR_REDIRECTS, false);
            dc.getParams().setParameter(ClientPNames.HANDLE_REDIRECTS, true);
            dc.setRedirectHandler(new DefaultRedirectHandler() { 

                public boolean isRedirectRequested(HttpResponse response, HttpContext context) { 
                    boolean ret = super.isRedirectRequested(response, context);
                    return ret; 
                } 

                public URI getLocationURI(HttpResponse response, HttpContext context) throws ProtocolException { 
                    URI uri = super.getLocationURI(response, context);
                    return uri;
                } 

            });
            dc.addRequestInterceptor(new HttpRequestInterceptor() {
                public void process(HttpRequest request, HttpContext context) {
                    for (String header : clientHeaderMap.keySet()) {
                        request.addHeader(header, clientHeaderMap.get(header));
                    }

                    HttpUriRequest req = null;
                    if (request instanceof EntityEnclosingRequestWrapper){
                        req = ((HttpUriRequest)((EntityEnclosingRequestWrapper)request).getOriginal());
                    }else if (request instanceof RequestWrapper){
                        req = ((HttpUriRequest)((RequestWrapper)request).getOriginal());
                    }
                }
            });
        }

        clientHeaderMap = new HashMap<String, String>();

    }

    public HttpClient getHttpClient(){
        return client; 
    }

    public void setHttpClient(HttpClient client){
        this.client = client; 
    }

    public void addHeader(String header, String value) {
        clientHeaderMap.put(header, value);
    }

    public void setApiHost(final String host){
        this.host = host;
    }

    public String url(String path){
        return url(path, false); 
    }

    public String url(String path, boolean https){
        return https ? String.format("https://%s%s", host, path) : String.format("http://%s%s", host, path); 
    }

    private String urlWithQueryString(String url, RequestParams params) {
        if(params != null) {
            String paramString = params.getParamString();
            url += "?" + paramString;
        }
        Log.d(TAG, url);
        return url;
    }

    public String parseResponse(HttpResponse response) throws ApiError, IOException {
        String body = null;
        StatusLine status = response.getStatusLine();
        int code = status.getStatusCode();

        HttpEntity entity = null;
        HttpEntity temp = response.getEntity();
        if(temp != null) {
            entity = new BufferedHttpEntity(temp);
        }
        body = EntityUtils.toString(entity, "UTF-8");
        Log.d(TAG, "resp: " + body);
        if (status.getStatusCode() >= 300){
            throw new ApiError(code, body);
        }
        return body;
    }

    public String getString(String url, RequestParams params) throws ApiError, IOException{
        final HttpGet req = new HttpGet(urlWithQueryString(url, params));
        return parseResponse(client.execute(req));
    }

    /**
     * Perform a HTTP GET request without parameters.
     * @param url the URL to send the request to.
     */
    public JSONObject get(String url) throws ApiError, IOException, JSONException{
        return get(url, null);
    }

    /**
     * Perform a HTTP GET request with parameters.
     * @param url the URL to send the request to.
     * @param params additional GET parameters to send with the request.
     */
    public JSONObject get(String url, RequestParams params) throws ApiError, IOException, JSONException{
        return new JSONObject(getString(url, params));
    }

    /**
     * @param url
     * @param params
     * @return
     * @throws ApiError
     * @throws IOException
     * @throws JSONException
     */
    public JSONObject post(String url, RequestParams params) throws ApiError, IOException, JSONException{
        final HttpPost req = new HttpPost(url);
        if(params != null) req.setEntity(params.getEntity());
        return new JSONObject(parseResponse(client.execute(req)));
    }

    /**
     * Perform a HTTP PUT request with parameters.
     * @param url the URL to send the request to.
     * @param params additional PUT parameters or files to send with the request.
     */
    public JSONObject put(String url, RequestParams params) throws ApiError, IOException, JSONException{
        final HttpPut req = new HttpPut(url);
        if(params != null) req.setEntity(params.getEntity());
        return new JSONObject(parseResponse(client.execute(req)));
    }

    /**
     * Perform a HTTP DELETE request.
     * @param url the URL to send the request to.
     */
    public JSONObject delete(String url) throws ApiError, IOException, JSONException{
        final HttpDelete req = new HttpDelete(url);
        Log.d(TAG, url);
        return new JSONObject(parseResponse(client.execute(req)));
    }

}

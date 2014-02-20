package com.demo.maker;

import android.app.Application;

import android.content.Context;
import android.content.Intent;

import android.graphics.Bitmap;

import android.os.Environment;

import com.demo.maker.model.Env;

import com.nostra13.universalimageloader.cache.disc.impl.TotalSizeLimitedDiscCache;
import com.nostra13.universalimageloader.cache.disc.naming.Md5FileNameGenerator;
import com.nostra13.universalimageloader.core.DisplayImageOptions;
import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;
import com.nostra13.universalimageloader.core.assist.ImageLoadingListener;
import com.nostra13.universalimageloader.core.assist.ImageScaleType;
import com.nostra13.universalimageloader.core.assist.PauseOnScrollListener;
import com.nostra13.universalimageloader.core.assist.QueueProcessingType;
import com.nostra13.universalimageloader.core.display.FadeInBitmapDisplayer;

import java.io.File;
import java.io.IOException;

public class DemoApp extends Application {

    public static final String IMAGE_CACHE_DIR = "images";
    public static final int IMAGE_CACHE_DISC_SIZE = 200 * 1024 * 1024;
    public static final String NO_MEDIA = ".nomedia";

    public static File getCacheDir(Context context) {
        if (Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState())) {
            File cacheDir = context.getExternalCacheDir();
            File noMedia = new File(cacheDir, NO_MEDIA);
            if (!noMedia.exists()) {
                try {
                    noMedia.createNewFile();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return cacheDir;
        } else {
            return context.getCacheDir();
        }
    }

    public static File getImageCacheDir(Context context) {
        File imageCacheDir = new File(getCacheDir(context), IMAGE_CACHE_DIR);
        if (!imageCacheDir.exists()) {
            imageCacheDir.mkdirs();
        }
        return imageCacheDir;
    }

    @Override
    public void onCreate() {
        super.onCreate();

        DisplayImageOptions options = new DisplayImageOptions.Builder()
                .bitmapConfig(Bitmap.Config.RGB_565)
                .imageScaleType(ImageScaleType.IN_SAMPLE_POWER_OF_2)
                .cacheInMemory(true)
                .cacheOnDisc(true)
                .resetViewBeforeLoading()
                .build();

        ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(this)
                .threadPoolSize(6)
                .memoryCacheSizePercentage(50)
                .defaultDisplayImageOptions(options)
                .denyCacheImageMultipleSizesInMemory()
                .tasksProcessingOrder(QueueProcessingType.FIFO)
                .discCache(new TotalSizeLimitedDiscCache(
                            getImageCacheDir(this), new Md5FileNameGenerator(), IMAGE_CACHE_DISC_SIZE
                            )
                        )
                .build();

        ImageLoader.getInstance().init(config);
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        ImageLoader.getInstance().clearMemoryCache();
    }

    @Override
    public void onTerminate() {
        super.onTerminate();
    }

    public static void startPage(Context context, Env env, String toId){
        startPage(context, env, "0", toId);
    }

    public static void startPage(Context context, Env env, String fromId, String toId){
        Intent it = new Intent(context, Runner.class);
        //Intent it = new Intent(context, Page.class);
        it.putExtra("env", env.toString());
        it.putExtra("refer", fromId);
        it.putExtra("id", toId);
        context.startActivity(it); 
    }

}

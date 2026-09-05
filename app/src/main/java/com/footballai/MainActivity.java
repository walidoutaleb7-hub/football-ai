package com.footballai;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {

    private WebView webView;
    private long exitTime = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // تفعيل الشاشة الكاملة (تمتد تحت شريط الحالة)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            getWindow().getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            );
        }

        // تثبيت الاتجاه العمودي (منع الدوران)
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        // إنشاء WebView
        webView = new WebView(this);
        WebSettings settings = webView.getSettings();

        // إعدادات أساسية
        settings.setJavaScriptEnabled(true);               // تفعيل JavaScript
        settings.setDomStorageEnabled(true);               // تفعيل LocalStorage
        settings.setDatabaseEnabled(true);                 // تفعيل IndexedDB
        settings.setAllowFileAccess(true);                 // السماح بالوصول للملفات
        settings.setAllowContentAccess(true);              // السماح بمحتوى ContentProvider
        settings.setLoadWithOverviewMode(true);            // عرض الصفحة كاملة
        settings.setUseWideViewPort(true);                 // دعم العرض الكامل
        settings.setBuiltInZoomControls(false);            // إلغاء التحكم بالتكبير
        settings.setDisplayZoomControls(false);            // إخفاء أزرار التكبير

        // 🔥 الحل السحري لظهور الصور من الإنترنت في الملف المحلي
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
            settings.setAllowUniversalAccessFromFileURLs(true);
        }

        // معالج الروابط: تبقى داخل التطبيق (لا تفتح المتصفح)
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        // معالج الإشعارات (لتنبيهات JavaScript)
        webView.setWebChromeClient(new WebChromeClient());

        // تحميل ملف اللعبة من مجلد assets
        webView.loadUrl("file:///android_asset/index.html");

        // عرض الـ WebView كواجهة التطبيق
        setContentView(webView);
    }

    // معالج زر الرجوع: العودة للصفحة السابقة داخل اللعبة
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            // خروج مزدوج (اضغط مرتين خلال ثانيتين للخروج)
            if (System.currentTimeMillis() - exitTime < 2000) {
                finish();
            } else {
                Toast.makeText(this, "اضغط مرة أخرى للخروج", Toast.LENGTH_SHORT).show();
                exitTime = System.currentTimeMillis();
            }
        }
    }

    // استعادة الشاشة الكاملة عند العودة للتطبيق من الخلفية
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus && Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            getWindow().getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            );
        }
    }
}
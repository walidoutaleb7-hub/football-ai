
package com.footballai;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {

    private WebView webView;
    private long exitTime = 0; // للخروج المزدوج

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // تفعيل الشاشة الكاملة (تمتد إلى شريط الحالة)
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

        // تثبيت اتجاه الشاشة (منع الدوران)
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        webView = new WebView(this);
        WebSettings settings = webView.getSettings();

        // تمكين JavaScript (ضروري للعبة)
        settings.setJavaScriptEnabled(true);

        // تمكين التخزين المحلي (LocalStorage)
        settings.setDomStorageEnabled(true);

        // تمكين التخزين عبر IndexedDB (اختياري)
        settings.setDatabaseEnabled(true);

        // تمكين استخدام ذاكرة التخزين المؤقت (Cache)
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        // السماح بتحميل الصور والملفات من assets
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        // تحسين تجربة العرض
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);

        // تمكين التكبير/التصغير (اختياري، لكن الأفضل تعطيله للعبة)
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        // دعم الصور عالية الدقة
        settings.setSupportZoom(false);

        // معالج الروابط: تبقى داخل WebView (بدلاً من فتح المتصفح)
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                view.loadUrl(request.getUrl().toString());
                return true; // لا نفتح في متصفح خارجي
            }

            // عرض رسالة عند فشل تحميل الصفحة
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                Toast.makeText(MainActivity.this, "تعذر تحميل اللعبة. تحقق من اتصالك بالإنترنت.", Toast.LENGTH_LONG).show();
            }
        });

        // معالج الإشعارات (مثل تنبيهات JavaScript)
        webView.setWebChromeClient(new WebChromeClient());

        // تحميل ملف اللعبة من مجلد assets
        webView.loadUrl("file:///android_asset/index.html");

        setContentView(webView);
    }

    // معالجة زر الرجوع: العودة للصفحة السابقة أو الخروج من التطبيق
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            // خروج مزدوج (إذا ضغط مرتين خلال ثانيتين، يخرج)
            if (System.currentTimeMillis() - exitTime < 2000) {
                finish();
            } else {
                Toast.makeText(this, "اضغط مرة أخرى للخروج", Toast.LENGTH_SHORT).show();
                exitTime = System.currentTimeMillis();
            }
        }
    }

    // استعادة الشاشة الكاملة عند العودة للتطبيق
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
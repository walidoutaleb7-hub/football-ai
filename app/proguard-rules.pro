# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

-dontwarn org.apache.http.**
-dontwarn android.webkit.WebView
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
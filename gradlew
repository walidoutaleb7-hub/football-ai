#!/bin/bash

##############################################################################
##
##  Gradle start up script for UN*X
##
##############################################################################

# Attempt to set APP_HOME
# Resolve links: $0 may be a symlink
PRG="$0"
# Need this for relative symlinks.
while [ -h "$PRG" ] ; do
    ls -ld "$PRG"
    link=`ls -l "$PRG" | awk '{print $NF}'`
    case $link in
        /*) PRG="$link";;
        *) PRG=`dirname "$PRG"`"/$link";;
    esac
done
SAVED="`pwd`"
cd "`dirname \"$PRG\"`/" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

APP_NAME="Gradle"
APP_BASE_NAME=`basename "$0"`

# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD="maximum"

warn ( ) {
    echo "$*"
}

die ( ) {
    echo
    echo "$*"
    echo
    exit 1
}

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "`uname`" in
  CYGWIN* )
    cygwin=true
    ;;
  Darwin* )
    darwin=true
    ;;
  MINGW* )
    msys=true
    ;;
  NONSTOP* )
    nonstop=true
    ;;
esac

# Determine the Java command to use to start the JVM.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        # IBM's JDK on AIX uses strange locations for the executables
        JAVACMD="$JAVA_HOME/jre/sh/java"
    else
        JAVACMD="$JAVA_HOME/bin/java"
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
    fi
else
    JAVACMD="java"
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
fi

# Increase the maximum file descriptors if we can.
if [ "$cygwin" = "false" -a "$darwin" = "false" -a "$nonstop" = "false" ] ; then
    MAX_FD_LIMIT=`ulimit -H -n`
    if [ $? -eq 0 ] ; then
        if [ "$MAX_FD" = "maximum" -o "$MAX_FD" = "max" ] ; then
            MAX_FD="$MAX_FD_LIMIT"
        fi
        ulimit -n $MAX_FD
        if [ $? -ne 0 ] ; then
            warn "Could not set maximum file descriptor limit: $MAX_FD"
        fi
    else
        warn "Could not query maximum file descriptor limit: $MAX_FD_LIMIT"
    fi
fi

# For Darwin, add options to specify how the application appears in the dock
if $darwin; then
    GRADLE_OPTS="$GRADLE_OPTS \"-Xdock:name=$APP_NAME\" \"-Xdock:icon=$APP_HOME/media/gradle.icns\""
fi

# For Cygwin or MSYS, switch paths to Windows format before running java
if [ "$cygwin" = "true" -o "$msys" = "true" ] ; then
    APP_HOME=`cygpath --path --mixed "$APP_HOME"`
    CLASSPATH=`cygpath --path --mixed "$CLASSPATH"`

    JAVACMD=`cygpath --unix "$JAVACMD"`

    # We build the pattern for arguments to be converted via cygpath
    ROOTDIRSRAW=`find -L / -maxdepth 3 -type d -name gradle 2>/dev/null`
    [ -z "$ROOTDIRSRAW" ] && ROOTDIRSRAW=`find -L / -maxdepth 3 -type f -name gradle 2>/dev/null`
    for dir in $ROOTDIRSRAW ; do
        ROOTDIR=`dirname "$dir"`
        if [ -d "$ROOTDIR" ] ; then
            ROOTDIR_FOUND=true
            break
        fi
    done
    if [ -z "$ROOTDIR" -o ! -d "$ROOTDIR" ] ; then
        # attempt using $ which
        ROOTDIR=`dirname \`which gradle\` 2>/dev/null`
    fi
fi
# Oops, we failed, let's try using $JAVA_HOME and hope it's valid
if [ -z "$ROOTDIR" -o ! -d "$ROOTDIR" ] ; then
    if [ -x "$JAVA_HOME/bin/java" ] ; then
        ROOTDIR=`dirname \`"$JAVA_HOME"/bin/java -version 2>&1 | grep java.home | awk '{print $NF}' | sed 's/\/bin\/java.*//' 2>/dev/null\` 2>/dev/null`
    fi
fi
if [ -z "$ROOTDIR" -o ! -d "$ROOTDIR" ] ; then
    die "Unable to determine Gradle root directory."
fi

# if we get here and GRADLE_HOME is still empty
if [ -z "$GRADLE_HOME" ] ; then
    GRADLE_HOME="$ROOTDIR"
fi

# By default we should be in the correct project dir, but when run from Finder on Mac, the cwd may not be the project dir
if [ "$HOME" = "$OLDPWD" ] ; then
    cd "`dirname \"$0\"`"
fi

exec "$JAVACMD" $DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS -classpath "`classpath`" org.gradle.wrapper.GradleWrapperMain "$@"

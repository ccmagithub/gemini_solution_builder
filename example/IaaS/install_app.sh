#!/bin/bash

# *** shell script for Solution Foundry to add an app ***
# Step  1: install app's logo
# Step  2: install template files (~.html files)
# Step  3: install js files if there are js files in package folder
# Step  4: install css files if there are css files in package folder
# Step  5: install app's files (~.py files)
# Step  6: add app to INSTALLED_APPS in settings.py
# Step  7: include app's urls.py to project's urls.py
# Step  8: sync GOC Portal Solution list to Service Portal
# Step  9: database migrate
# Step 10: chown to www-data for Service Portal Django project folder
# (if exception happens in Step x, Step 1 ~ Step x-1 oprations will rollback)
# *** end ***

function error_exit
{
    echo "$1" 1>&2
    exit 1
}

# < get service name from argument and convert it to lowercase >
# if [ -z "$1" ]; then
#     error_exit "Please input Service Name"
# fi
# SERVICE_NAME=$1
# LOWER_NAME=`echo $SERVICE_NAME | tr '[:upper:]' '[:lower:]'`
SERVICE_NAME="IaaS"
LOWER_NAME="iaas"

# < get package root path from argument >
# if [ -z "$2" ]; then
#     error_exit "Please input package's root path"
# fi
# PACKAGE_ROOT=$2
PACKAGE_ROOT=$1
if [ "${PACKAGE_ROOT: -1}" = "/" ]; then
    PACKAGE_ROOT="${PACKAGE_ROOT::-1}"
fi

# Service Portal folder path vars
PROJECT_ROOT="/usr/share/sportal"
STATIC_ROOT="${PROJECT_ROOT}/static"
TEMPLATES_ROOT="${PROJECT_ROOT}/templates"
APP_ROOT="${PROJECT_ROOT}/sportal"
JS_ROOT="${STATIC_ROOT}/js"
CSS_ROOT="${STATIC_ROOT}/css"
IMG_ROOT="${STATIC_ROOT}/img"

# < Step 1: service logo >
IMG_PATH="${IMG_ROOT}/service_logo/${LOWER_NAME}"
if [ -d "${IMG_PATH}" ]; then
    error_exit "${IMG_PATH} exists. Aborting..."
else
    if [ "$(ls -A ${PACKAGE_ROOT}/img)" ]; then
        mkdir ${IMG_PATH}
        if cp -r ${PACKAGE_ROOT}/img/* ${IMG_PATH}; then
            echo "Service logo files have been installed"
        else
            # rollback
            rm -r ${IMG_PATH}
            error_exit "Install service logo files unsuccessfully. Aborting..."
        fi
    else
        error_exit "Cannot find service logo files. Aborting..."
    fi
fi

# < Step 2: template files (~.html) >
TEMPLATES_PATH="${TEMPLATES_ROOT}/service/${LOWER_NAME}"
if [ -d "${TEMPLATES_PATH}" ]; then
    # rollback
    rm -r ${IMG_PATH}
    error_exit "${TEMPLATES_PATH} exists. Aborting..."
else
    if [ "$(ls -A ${PACKAGE_ROOT}/templates)" ]; then
        mkdir ${TEMPLATES_PATH}
        if cp -r ${PACKAGE_ROOT}/templates/* ${TEMPLATES_PATH}; then
            echo "Template files have been installed"
        else
            # rollback
            rm -r ${IMG_PATH}
            rm -r ${TEMPLATES_PATH}
            error_exit "Install template files unsuccessfully. Aborting..."
        fi
    else
        error_exit "Cannot find template files. Aborting..."
    fi
fi

# < Step 3: js files >
JS_PATH="${JS_ROOT}/service/${LOWER_NAME}"
if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
    if [ -d "${JS_PATH}" ]; then
        # rollback
        rm -r ${IMG_PATH}
        rm -r ${TEMPLATES_PATH}
        error_exit "${JS_PATH} exists. Aborting..."
    else
        mkdir ${JS_PATH}
        if cp -r ${PACKAGE_ROOT}/js/* ${JS_PATH}; then
            echo "js files have been installed"
        else
            # rollback
            rm -r ${IMG_PATH}
            rm -r ${TEMPLATES_PATH}
            rm -r ${JS_PATH}
            error_exit "Install js files unsuccessfully. Aborting..."
        fi
    fi
else
    echo "No need to install js files"
fi

# < Step 4: css files >
CSS_PATH="${CSS_ROOT}/service/${LOWER_NAME}"
if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
    if [ -d "${CSS_PATH}" ]; then
        # rollback
        rm -r ${IMG_PATH}
        rm -r ${TEMPLATES_PATH}
        if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
            rm -r ${JS_PATH}
        fi
        error_exit "${CSS_PATH} exists. Aborting..."
    else
        mkdir ${CSS_PATH}
        if cp -r ${PACKAGE_ROOT}/css/* ${CSS_PATH}; then
            echo "css files have been installed"
        else
            # rollback
            rm -r ${IMG_PATH}
            rm -r ${TEMPLATES_PATH}
            if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
                rm -r ${JS_PATH}
            fi
            rm -r ${CSS_PATH}
            error_exit "Install css files unsuccessfully. Aborting..."
        fi
    fi
else
    echo "No need to install css files"
fi

# < Step 5: app files (~.py) >
APP_PATH="${APP_ROOT}/service/${LOWER_NAME}"
if [ -d "${APP_PATH}" ]; then
    # rollback
    rm -r ${IMG_PATH}
    rm -r ${TEMPLATES_PATH}
    if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
        rm -r ${JS_PATH}
    fi
    if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
        rm -r ${CSS_PATH}
    fi
    error_exit "${APP_PATH} exists. Aborting..."
else
    if [ "$(ls -A ${PACKAGE_ROOT}/app)" ]; then
        mkdir ${APP_PATH}
        if cp -r ${PACKAGE_ROOT}/app/* ${APP_PATH}; then
            echo "app files have been installed"
        else
            # rollback
            rm -r ${IMG_PATH}
            rm -r ${TEMPLATES_PATH}
            if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
                rm -r ${JS_PATH}
            fi
            if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
                rm -r ${CSS_PATH}
            fi
            rm -r ${APP_PATH}
            error_exit "Install app files unsuccessfully. Aborting..."
        fi
    else
        error_exit "Cannot find app files. Aborting..."
    fi
fi

# < Step 6: add app to settings.py >
SETTINGS_PATH="${APP_ROOT}/settings.py"
NEW_INSTALLED_APPS_TEXT="'sportal.service.$LOWER_NAME'"
if sed -i "/INSTALLED_APPS/a \ \ \ \ ${NEW_INSTALLED_APPS_TEXT}," ${SETTINGS_PATH}; then
    echo "add app to INSTALLED_APPS successfully"
else
    # rollback
    rm -r ${IMG_PATH}
    rm -r ${TEMPLATES_PATH}
    if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
        rm -r ${JS_PATH}
    fi
    if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
        rm -r ${CSS_PATH}
    fi
    rm -r ${APP_PATH}
    error_exit "Add app to INSTALLED_APPS unsuccessfully. Aborting..."
fi

# < Step 7: include app's urlpatterns to urls.py >
URLS_PATH="${APP_ROOT}/urls.py"
IMPORT_URLS_FILE_TEXT="from service.${LOWER_NAME} import urls as ${LOWER_NAME}_urls"
INCLUDE_URLPATTERNS_TEXT="url(r'^${LOWER_NAME}/', include(${LOWER_NAME}_urls.urlpatterns), kwargs={'service_name': '${SERVICE_NAME}'})"
if sed -i "/from sportal.service import views as service_views/a ${IMPORT_URLS_FILE_TEXT}" ${URLS_PATH}; then
    echo "Import urls file successfully"
    if sed -i "/# services/a \ \ \ \ ${INCLUDE_URLPATTERNS_TEXT}," ${URLS_PATH}; then
        echo "Include url patterns successfully"
    else
        # rollback
        rm -r ${IMG_PATH}
        rm -r ${TEMPLATES_PATH}
        if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
            rm -r ${JS_PATH}
        fi
        if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
            rm -r ${CSS_PATH}
        fi
        rm -r ${APP_PATH}
        sed -i "/${NEW_INSTALLED_APPS_TEXT}/d" ${SETTINGS_PATH}
        sed -i "/${IMPORT_URLS_FILE_TEXT}/d" ${URLS_PATH}
        error_exit "Include url patterns unsuccessfully. Aborting..."
    fi
else
    # rollback
    rm -r ${IMG_PATH}
    rm -r ${TEMPLATES_PATH}
    if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
        rm -r ${JS_PATH}
    fi
    if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
        rm -r ${CSS_PATH}
    fi
    rm -r ${APP_PATH}
    sed -i "/${NEW_INSTALLED_APPS_TEXT}/d" ${SETTINGS_PATH}
    error_exit "Import service urls unsuccessfully. Aborting..."
fi

# < Step 8: sync GOC Portal Solutions to Service Portal >
cd ${PROJECT_ROOT}
if python -c 'import init_util; init_util.sync_admin_role_user_service()'; then
    echo "Sync GOC Portal Solution list successfully"
else
    # rollback
    rm -r ${IMG_PATH}
    rm -r ${TEMPLATES_PATH}
    if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
        rm -r ${JS_PATH}
    fi
    if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
        rm -r ${CSS_PATH}
    fi
    rm -r ${APP_PATH}
    sed -i "/${NEW_INSTALLED_APPS_TEXT}/d" ${SETTINGS_PATH}
    sed -i "/${IMPORT_URLS_FILE_TEXT}/d" ${URLS_PATH}
    sed -i "/${INCLUDE_URLPATTERNS_TEXT}/d" ${URLS_PATH}
    error_exit "Sync GOC Portal Solution list unsuccessfully"
fi

# < Step 9: database migration >
if python ${PROJECT_ROOT}/manage.py migrate; then
    echo "Database migrate successfully"
else
    # rollback
    rm -r ${IMG_PATH}
    rm -r ${TEMPLATES_PATH}
    if [ "$(ls -A ${PACKAGE_ROOT}/js)" ]; then
        rm -r ${JS_PATH}
    fi
    if [ "$(ls -A ${PACKAGE_ROOT}/css)" ]; then
        rm -r ${CSS_PATH}
    fi
    rm -r ${APP_PATH}
    sed -i "/${NEW_INSTALLED_APPS_TEXT}/d" ${SETTINGS_PATH}
    sed -i "/${IMPORT_URLS_FILE_TEXT}/d" ${URLS_PATH}
    sed -i "/${INCLUDE_URLPATTERNS_TEXT}/d" ${URLS_PATH}
    error_exit "Database migrate unsuccessfully. Aborting..."
fi

# < Step 10: chown to www-data for Service Portal Django project folder >
chown -R www-data:www-data ${PROJECT_ROOT}

echo "Done"

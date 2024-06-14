"""This module provides the GPOAnalyzer config data."""
# gpoanalyzer/gpo_value_paths.py

gpo_value_paths = {
    "shortcuts": {
        # "clsid": "clsid",
        # "userContext": "userContext",
        "name": "name",
        "status": "status",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        # "pidl": "Properties.pidl",
        # "targetType": "Properties.targetType",
        # "action": "Properties.action",
        # "comment": "Properties.comment",
        # "shortcutKey": "Properties.shortcutKey",
        # "startIn": "Properties.startIn",
        # "arguments": "Properties.arguments",
        # "iconIndex": "Properties.iconIndex",
        "targetPath": "Properties.targetPath",
        # "iconPath": "Properties.iconPath",
        # "window": "Properties.window",
        # "shortcutPath": "Properties.shortcutPath"
    },
    "scheduledtasks": {
        "name": "name",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        # "userContext": "userContext",
        # "removePolicy": "removePolicy",
        "disabled": "disabled",
        "action": "Properties.action",

        "runAs": "Properties.runAs",
        "logonType": "Properties.logonType",

        # "version": "Properties.Task.version",
        # "id": "Properties.Task.Principals.Principal.id",
        # "Context": "Properties.Task.Actions.Context"

        "command": "Properties.Task.Actions.Exec.Command._text",
        "arguments": "Properties.Task.Actions.Exec.Arguments._text",
    },
    "drives": {
        # "clsid": "clsid",
        "name": "name",
        "status": "status",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        # "userContext": "userContext",
        # "bypassErrors": "bypassErrors",
        "action": "Properties.action",
        # "thisDrive": "Properties.thisDrive",
        # "allDrives": "Properties.allDrives",
        "userName": "Properties.userName",
        "path": "Properties.path",
        # "label": "Properties.label",
        # "persistent": "Properties.persistent",
        # "useLetter": "Properties.useLetter",
        # "letter": "Properties.letter",
        "FilterUser": "Filters.FilterUser"
    },
    "groups": {
        # GROUP
        # 'clsid': 'clsid',
        'name': 'name',
        # "image": "image",
        'changed': 'changed',
        # "uid": "uid",
        # "userContext": "userContext",
        # "removePolicy": "removePolicy",
        # "desc": "desc",
        # "action": "Properties.Members.Member.action",
        # "newName": "Properties.newName",
        # "description": "Properties.description",
        # "deleteAllUsers": "Properties.deleteAllUsers",
        # "deleteAllGroups": "Properties.deleteAllGroups",
        # "removeAccounts": "Properties.removeAccounts",
        # 'group_sid': 'Properties.groupSid',
        # "groupName": "Properties.groupName",
        # "sid": "Properties.Members.Member.sid",

        'FilterComputer': 'Filters.FilterComputer',
        'member': 'Properties.Members.Member',

        # USER
        # "clsid": "clsid",
        # "name": "name",
        # "image": "image",
        # "changed": "changed",
        # "uid": "uid",
        # "userContext": "userContext",
        # "removePolicy": "removePolicy",
        # "action": "Properties.action",
        "newName": "Properties.newName",
        "fullName": "Properties.fullName",
        "description": "Properties.description",
        'cpassword': 'Properties.cpassword',
        # "changeLogon": "Properties.changeLogon",
        # "noChange": "Properties.noChange",
        "neverExpires": "Properties.neverExpires",
        "acctDisabled": "Properties.acctDisabled",
        # "subAuthority": "Properties.subAuthority",
        "userName": "Properties.userName",
        # "hidden": "Filters.FilterRunOnce.hidden",
        # "not": "Filters.FilterRunOnce.not",
        # "bool": "Filters.FilterRunOnce.bool",
        # "id": "Filters.FilterRunOnce.id"
    },
    "printers": {
        # "clsid": "clsid",
        "changed": "changed",
        "disabled": "disabled",
        "status": "status",
        "snmpCommunity": "Properties.snmpCommunity",
        "snmpEnabled": "Properties.snmpEnabled",
        "portNumber": "Properties.portNumber",
        "ipAddress": "Properties.ipAddress",
        "localName": "Properties.localName",
        "comment": "Properties.comment",
        "path": "Properties.path",
        "FilterGroup": "Filters.FilterGroup",
        # "image": "image",
        # "uid": "uid",
        # "bypassErrors": "bypassErrors",
        # "lprQueue": "Properties.lprQueue",
        # "protocol": "Properties.protocol",
        # "doubleSpool": "Properties.doubleSpool",
        # "snmpDevIndex": "Properties.snmpDevIndex",
        # "action": "Properties.action",
        # "location": "Properties.location",
        # "default": "Properties.default",
        # "skipLocal": "Properties.skipLocal",
        # "useDNS": "Properties.useDNS",
        # "useIPv6": "Properties.useIPv6",
        # "deleteAll": "Properties.deleteAll",
    },
    "registryxml": {
        # "clsid": "clsid",
        "name": "Properties.name",
        "status": "status",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        "action": "Properties.action",
        # "displayDecimal": "Properties.displayDecimal",
        "default": "Properties.default",
        "hive": "Properties.hive",
        "key": "Properties.key",
        "type": "Properties.type",
        "value": "Properties.value"
    },
    "envvars": {
        # "clsid": "clsid",
        "name": "Properties.name",
        "status": "status",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        "userContext": "userContext",
        # "bypassErrors": "bypassErrors",
        "action": "Properties.action",
        "value": "Properties.value",
        "user": "Properties.user",
        "partial": "Properties.partial"
    },
    "files": {
        # "clsid": "clsid",
        "name": "name",
        "status": "status",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        "action": "Properties.action",
        "fromPath": "Properties.fromPath",
        "targetPath": "Properties.targetPath",
        "readOnly": "Properties.readOnly",
        "archive": "Properties.archive",
        "hidden": "Properties.hidden"
    },
    "services": {
        # "clsid": "clsid",
        "name": "name",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        "userContext": "userContext",
        # "removePolicy": "removePolicy",
        "startupType": "Properties.startupType",
        "serviceName": "Properties.serviceName",
        "serviceAction": "Properties.serviceAction",
        # "timeout": "Properties.timeout"
    },
    "folders": {
        # "clsid": "clsid",
        "name": "name",
        "status": "status",
        # "image": "image",
        "changed": "changed",
        # "uid": "uid",
        # "userContext": "userContext",
        # "bypassErrors": "bypassErrors",
        "action": "Properties.action",
        "path": "Properties.path",
        "readOnly": "Properties.readOnly",
        "archive": "Properties.archive",
        "hidden": "Properties.hidden"
    },
    "internetsettings": {
        # "clsid": "Collection.Registry.clsid",
        "name": "Collection.Registry.Properties.name",
        "status": "status",
        "changed": "changed",
        # "uid": "uid",
        # "userContext": "userContext",
        # "bypassErrors": "bypassErrors",
        # "hidden": "Filters.FilterFile.hidden",
        # "not": "Filters.FilterFile.not",
        # "bool": "Filters.FilterFile.bool",
        # "path": "Filters.FilterFile.path",
        "type": "Collection.Registry.Properties.type",
        # "gte": "Filters.FilterFile.gte",
        # "min": "Filters.FilterFile.min",
        # "max": "Filters.FilterFile.max",
        # "lte": "Filters.FilterFile.lte",
        "disabled": "Collection.disabled",
        "action": "Collection.Registry.Properties.action",
        "default": "Collection.Registry.Properties.default",
        "hive": "Collection.Registry.Properties.hive",
        "key": "Collection.Registry.Properties.key",
        "value": "Collection.Registry.Properties.value",
        "Reg": "Properties.Reg",
    },
    "registrypol": "",
    "gpttmpl": ""
}

#coding: utf-8



ZBASES = {
    'journals': {
        'server': {
            'host': u'212.193.5.224',
            #'host': u'172.16.174.128',
            #'host': u'ns1.gbs.spb.ru',
            'port': u'210',
            #'user': u'erm',
            #'password': u'123456',
            'databaseName': u'KSOB',
            'preferredRecordSyntax': u'rusmarc',
         },
     }
}

SEARCH = {
    'min_term_length': 3, #минимальная длина поискового терма (зависит от настроек сервера)
}
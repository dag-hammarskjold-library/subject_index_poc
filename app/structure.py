# Definition of the body tag to manage

AUTH_TAG_VALUES=["A","T","S","E"]

# Definition of the authority tag to manage

AUTH_TAG_VALUES=[
                ('id','none'),
                ('191','a'),
                ('191','b'),
                ('191','d')
                ]

# Definition of the bibliographic tag to manage

BIB_TAG_VALUES=[
                ('id','none'),('191','9'),('191','a'),('191','b'),('191','c'),('239','a'),('245','a'),
                ('245','b'),('245','c'),('249','a'),('269','a'),('495','a'),('515','a'),('520','a'),
                ('598','none'),('599','a'),('930','a'),('991','a'),('991','d'),('991','e'),('991','z'),
                ('992','a'),('995','a'),('996','a')
                ]

# Definition of the label of all the tags

TAG_LABEL={ ('id','none'):'ID', 
            ('191','a'):'UN document symbol',
            ('191','b'):'Mainbody',
            ('191','d'):'Agenda subject',
            ('191','9'):'Header',
            ('191','a'):'Agenda document symbol',
            ('191','b'):'Agenda item number',
            ('191','c'):'Session',
            ('239','a'):'',
            ('245','a'):'Title',
            ('245','b'):'',
            ('245','c'):'',
            ('249','a'):'ITP Title',
            ('269','a'):'Pubdate (YYYYMMDD)',
            ('495','a'):'',
            ('515','a'):'',
            ('520','a'):'',
            ('598','none'):'',
            ('599','a'):'',
            ('930','a'):'UNBIS Product code and issue',
            ('991','a'):'Agenda document symbol',
            ('991','d'):'Agenda subject',
            ('991','e'):'',
            ('991','z'):'ITP Recordid',
            ('992','a'):'',
            ('995','a'):'',
            ('996','a'):''
          }

(self.webpackChunkupgradehub_frontend=self.webpackChunkupgradehub_frontend||[]).push([[7892],{91374:e=>{e.exports=function(e){var n="[ \\t\\f]*",a=n+"[:=]"+n,t="[ \\t\\f]+",r="("+a+"|"+t+")",s="([^\\\\\\W:= \\t\\f\\n]|\\\\.)+",i="([^\\\\:= \\t\\f\\n]|\\\\.)+",c={end:r,relevance:0,starts:{className:"string",end:/$/,relevance:0,contains:[{begin:"\\\\\\\\"},{begin:"\\\\\\n"}]}};return{name:".properties",case_insensitive:!0,illegal:/\S/,contains:[e.COMMENT("^\\s*[!#]","$"),{returnBegin:!0,variants:[{begin:s+a,relevance:1},{begin:s+t,relevance:0}],contains:[{className:"attr",begin:s,endsParent:!0,relevance:0}],starts:c},{begin:i+r,returnBegin:!0,relevance:0,contains:[{className:"meta",begin:i,endsParent:!0,relevance:0}],starts:c},{className:"attr",relevance:0,begin:i+n+"$"}]}}}}]);
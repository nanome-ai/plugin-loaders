(function(e){function t(t){for(var r,s,o=t[0],u=t[1],c=t[2],f=0,p=[];f<o.length;f++)s=o[f],Object.prototype.hasOwnProperty.call(a,s)&&a[s]&&p.push(a[s][0]),a[s]=0;for(r in u)Object.prototype.hasOwnProperty.call(u,r)&&(e[r]=u[r]);l&&l(t);while(p.length)p.shift()();return i.push.apply(i,c||[]),n()}function n(){for(var e,t=0;t<i.length;t++){for(var n=i[t],r=!0,o=1;o<n.length;o++){var u=n[o];0!==a[u]&&(r=!1)}r&&(i.splice(t--,1),e=s(s.s=n[0]))}return e}var r={},a={app:0},i=[];function s(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=r,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)s.d(n,r,function(t){return e[t]}.bind(null,r));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],u=o.push.bind(o);o.push=t,o=o.slice();for(var c=0;c<o.length;c++)t(o[c]);var l=u;i.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"0117":function(e,t,n){"use strict";var r=n("812f"),a=n.n(r);a.a},1140:function(e,t,n){"use strict";var r=n("fe45"),a=n.n(r);a.a},1146:function(e,t,n){},"1e7f":function(e,t,n){"use strict";var r=n("1146"),a=n.n(r);a.a},"21bb":function(e,t,n){"use strict";var r=n("7a98"),a=n.n(r);a.a},5258:function(e,t,n){},"56d7":function(e,t,n){"use strict";n.r(t);n("cadf"),n("551c"),n("f751"),n("097d"),n("def6");var r,a,i=n("2b0e"),s=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"w-screen h-screen",attrs:{id:"app"}},[n("router-view")],1)},o=[],u=(n("5c0b"),n("2877")),c={},l=Object(u["a"])(c,s,o,!1,null,null,null),f=l.exports,p=(n("a481"),n("8c4f")),d=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"home min-h-full container m-auto bg-white flex flex-col"},[e._m(0),n("p",{staticClass:"text-lg py-5"},[e._v("\n    Drag and drop or click the new file button to upload files."),n("br"),e._v("\n    Supports "),n("b",[e._v(e._s(e.extensions.join(" ")))])]),n("file-explorer")],1)},h=[function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("header",{staticClass:"pt-10 mx-auto"},[r("h1",{staticClass:"inline-flex items-baseline"},[r("img",{staticClass:"mr-4",attrs:{src:n("cf05")}}),e._v(" Vault\n    ")]),r("h2",[e._v("Upload files to make them available in Nanome!")])])}],m=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"file-explorer flex flex-col m-4 bg-gray-100 rounded flex-grow"},[n("div",{staticClass:"mx-4 mt-4 border-b"},[n("toolbar",{on:{"display-mode":function(t){e.displayMode=t},"new-folder":e.newFolder,"show-upload":e.showDropzone}}),n("breadcrumbs",{attrs:{path:e.path}})],1),n("div",{staticClass:"flex-grow relative select-none px-4",on:{contextmenu:function(t){return t.preventDefault(),e.showContextMenu({event:t,path:e.path})}}},["grid"===e.displayMode?n("file-view-grid",{ref:"grid",attrs:{path:e.path}}):n("file-view-list",{attrs:{path:e.path}}),n("file-dropzone",{ref:"dropzone",attrs:{path:e.path},on:{upload:e.refresh}})],1),n("div",{directives:[{name:"show",rawName:"v-show",value:e.contextmenu.show,expression:"contextmenu.show"},{name:"click-out",rawName:"v-click-out",value:e.hideContextMenu,expression:"hideContextMenu"}],staticClass:"contextmenu",style:{top:e.contextmenu.top,left:e.contextmenu.left}},[n("ul",["/"===e.contextmenu.path.slice(-1)?n("li",[n("button",{staticClass:"text-gray-800",on:{click:function(t){return e.newFolder(e.contextmenu.path)}}},[n("fa-icon",{attrs:{icon:"folder-plus"}}),e._v("\n          new folder\n        ")],1)]):e._e(),e.contextmenu.component?n("li",[n("button",{staticClass:"text-red-500",on:{click:e.deleteItem}},[n("fa-icon",{attrs:{icon:"trash"}}),e._v("\n          delete\n        ")],1)]):e._e()])])])},v=[],x=(n("96cf"),n("3b8d")),g=(n("ac4d"),n("8a81"),n("ac6a"),n("768b")),b={list:function(e){return fetch("/files"+e).then((function(e){return e.json()}))},getFolder:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n,r,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n={path:"",parent:"",files:[],folders:[]},"/"!==t.slice(-1)&&(t+="/"),"/"!==t&&(r=t.slice(0,-1).lastIndexOf("/"),n.parent=t.substring(0,r)+"/"),e.next=5,b.list(t);case 5:return a=e.sent,n.path=t,n.folders=a.folders,n.files=a.files.map((function(e){var t=/^(.+?)(?:\.(\w+))?$/.exec(e),n=Object(g["a"])(t,3),r=n[0],a=n[1],i=n[2];return{full:r,name:a,ext:i}})),e.abrupt("return",n);case 10:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}(),upload:function(e,t){if(t&&t.length){var n=new FormData,r=!0,a=!1,i=void 0;try{for(var s,o=t[Symbol.iterator]();!(r=(s=o.next()).done);r=!0){var u=s.value;n.append("file",u)}}catch(c){a=!0,i=c}finally{try{r||null==o.return||o.return()}finally{if(a)throw i}}return fetch("/files"+e,{method:"POST",body:n})}},delete:function(e){return fetch("/files"+e,{method:"DELETE"})},create:function(e){return fetch("/files"+e,{method:"POST"})}},w=b,y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"breadcrumbs flex text-xl py-3 items-center"},[n("router-link",{staticClass:"btn rounded mr-2",attrs:{to:e.parentPath,event:e.parentPath?"click":"",tabindex:e.parentPath?"":-1,disabled:!e.parentPath,tag:"button"}},[n("fa-icon",{attrs:{icon:"arrow-up"}})],1),e._l(e.subpaths.slice(0,-1),(function(t){var r=t.name,a=t.path;return n("div",{key:a},[n("router-link",{staticClass:"px-3",attrs:{to:a}},[e._v(e._s(r))]),n("fa-icon",{attrs:{icon:"angle-right"}})],1)})),n("div",{staticClass:"text-gray-600 px-3"},[e._v(e._s(e.currentName))])],2)},_=[],C=(n("7f7f"),n("28a5"),{props:{path:String},computed:{subpaths:function(){var e=this.path.slice(0,-1).split("/"),t=[],n="",r=!0,a=!1,i=void 0;try{for(var s,o=e[Symbol.iterator]();!(r=(s=o.next()).done);r=!0){var u=s.value;n+=u+"/",u||(u="files"),t.push({name:u,path:n})}}catch(c){a=!0,i=c}finally{try{r||null==o.return||o.return()}finally{if(a)throw i}}return t},currentName:function(){return this.subpaths[this.subpaths.length-1].name},parentPath:function(){if("/"==this.path)return"";var e=this.path.slice(0,-1).lastIndexOf("/");return this.path.slice(0,e)+"/"}}}),k=C,D=(n("e7ab"),Object(u["a"])(k,y,_,!1,null,null,null)),O=D.exports,j=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"toolbar flex text-lg items-center"},[n("div",{staticClass:"toggle relative mr-2 flex"},[n("input",{attrs:{checked:"",value:"grid",type:"radio",name:"display-mode",id:"display-mode-grid"},on:{input:function(t){return e.$emit("display-mode",t.target.value)}}}),n("label",{staticClass:"btn rounded-l",attrs:{for:"display-mode-grid"}},[n("fa-icon",{attrs:{icon:"th"}})],1),n("input",{attrs:{value:"list",type:"radio",name:"display-mode",id:"display-mode-list"},on:{input:function(t){return e.$emit("display-mode",t.target.value)}}}),n("label",{staticClass:"btn rounded-r",attrs:{for:"display-mode-list"}},[n("fa-icon",{attrs:{icon:"bars"}})],1)]),n("button",{staticClass:"btn rounded mr-2",on:{click:function(t){return e.$emit("new-folder")}}},[n("fa-layers",[n("fa-icon",{attrs:{icon:"folder"}}),n("fa-icon",{staticClass:"text-white",attrs:{icon:"plus",transform:"down-1 shrink-10"}})],1),n("span",{staticClass:"hidden lg:inline"},[e._v(" new folder")])],1),n("button",{staticClass:"btn rounded",on:{click:function(t){return e.$emit("show-upload")}}},[n("fa-icon",{attrs:{icon:"cloud-upload-alt"}}),n("span",{staticClass:"hidden lg:inline"},[e._v(" upload")])],1)])},E=[],$=(n("b751"),{}),R=Object(u["a"])($,j,E,!1,null,null,null),P=R.exports,S=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"file-view-grid-view pt-4 text-xl",class:{grid:e.files.length||e.folders.length}},[e._l(e.folders,(function(t){return n("router-link",{key:t,staticClass:"cursor-default",attrs:{title:t,to:""+e.path+t+"/",event:"dblclick"},nativeOn:{contextmenu:function(n){return n.preventDefault(),e.contextmenu(n,t+"/")}}},[n("fa-icon",{staticClass:"icon pointer-events-none",attrs:{icon:"folder"}}),n("div",{staticClass:"filename"},[e._v(e._s(t))])],1)})),e._l(e.files,(function(t){return n("div",{key:t.name,attrs:{title:t.full},on:{contextmenu:function(n){return n.preventDefault(),e.contextmenu(n,t.full)}}},[n("fa-layers",{staticClass:"icon"},[n("fa-icon",{attrs:{icon:"file"}}),n("fa-text",{staticClass:"text-white",attrs:{transform:"down-4 shrink-12",value:t.ext}})],1),n("div",{staticClass:"filename"},[e._v(e._s(t.name))])],1)})),e.files.length||e.folders.length?e._e():n("div",{staticClass:"text-xl py-4"},[e._v("\n    this folder is empty\n  ")])],2)},M=[],z={props:{path:String},data:function(){return{folders:[],files:[]}},watch:{path:{handler:"refresh",immediate:!0}},mounted:function(){this.$root.$on("refresh",this.refresh)},destroyed:function(){this.$root.$off("refresh",this.refresh)},methods:{refresh:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return this.beforeRefresh&&t&&this.beforeRefresh(),e.next=3,w.getFolder(this.path);case 3:n=e.sent,this.folders=n.folders,this.files=n.files;case 6:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}(),contextmenu:function(e,t){e.stopPropagation(),this.$root.$emit("contextmenu",{event:e,path:this.path+t,component:this})}}},F=z,L=Object(u["a"])(F,r,a,!1,null,null,null),T=L.exports,U={extends:T},N=U,H=(n("1140"),Object(u["a"])(N,S,M,!1,null,null,null)),I=H.exports,V=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"file-view-list-view text-xl"},[e.files.length||e.folders.length?n("ul",{staticClass:"w-full"},[e._l(e.folders,(function(t){return[n("li",{key:t,staticClass:"p-2 flex items-center"},[n("fa-icon",{staticClass:"text-2xl w-8 cursor-pointer text-gray-500 hover:text-black",class:{expanded:e.expanded[t]},attrs:{icon:"angle-right","fixed-width":""},on:{click:function(n){return e.toggleFolder(t)}}}),n("router-link",{staticClass:"file cursor-default",attrs:{title:t,to:""+e.path+t+"/",event:"dblclick"},nativeOn:{contextmenu:function(n){return n.preventDefault(),e.contextmenu(n,t+"/")}}},[n("fa-icon",{staticClass:"icon mr-2",attrs:{icon:e.expanded[t]?"folder-open":"folder"}}),n("div",{staticClass:"filename"},[e._v(e._s(t))])],1)],1),e.expanded[t]?n("li",{key:t+"-expanded",staticClass:"pl-8"},[n("file-view-list",{attrs:{path:""+e.path+t+"/",nested:""}})],1):e._e()]})),e._l(e.files,(function(t){return n("li",{key:t.name,staticClass:"p-2 file",attrs:{title:t.full},on:{contextmenu:function(n){return n.preventDefault(),e.contextmenu(n,t.full)}}},[n("div",{staticClass:"w-8"}),n("fa-layers",{staticClass:"icon mr-2"},[n("fa-icon",{attrs:{icon:"file"}}),n("fa-text",{staticClass:"text-white",attrs:{transform:"down-4 shrink-12",value:t.ext}})],1),n("div",{staticClass:"filename"},[e._v(e._s(t.full))])],1)}))],2):e.nested?e._e():n("div",{staticClass:"text-xl py-4"},[e._v("\n    this folder is empty\n  ")])])},A=[],B={extends:T,name:"file-view-list",components:{FileViewList:W},props:{nested:Boolean},data:function(){return{expanded:{}}},methods:{beforeRefresh:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:this.expanded={};case 1:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),toggleFolder:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:void 0===this.expanded[t]&&this.$set(this.expanded,t,!1),this.expanded[t]=!this.expanded[t];case 2:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}()}},G=B,J=(n("7bf6"),Object(u["a"])(G,V,A,!1,null,null,null)),W=J.exports,X=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{directives:[{name:"show",rawName:"v-show",value:e.showDropzone||e.isUploading,expression:"showDropzone || isUploading"}],staticClass:"file-dropzone",class:{hover:e.isHovering},on:{dragover:function(e){e.preventDefault()},dragenter:function(t){t.preventDefault(),e.isHovering=!0},dragleave:function(t){if(t.preventDefault(),t.target!==t.currentTarget)return null;e.isHovering=!1},drop:function(t){return t.preventDefault(),e.onDrop(t)}}},[n("label",{staticClass:"message m-4"},[n("input",{ref:"input",staticClass:"visually-hidden",attrs:{accept:e.extensions.join(","),type:"file",multiple:""},on:{change:e.onChange}}),n("div",{staticClass:"text-4xl"},[e.isUploading?[e._v("\n        Uploading files...\n      ")]:e.numDropping?[e._v("\n        Drop "+e._s(e.numDropping)+" item"+e._s(e.numDropping>1?"s":"")+" here to\n        upload\n      ")]:[e._v("\n        Drop items or\n        "),n("span",{staticClass:"text-blue-500"},[e._v("click")]),e._v("\n        to upload\n      ")]],2),e.numDropping||e.isUploading?e._e():n("button",{staticClass:"text-2xl text-red-500",on:{click:function(t){e.showDropzone=!1}}},[e._v("\n      cancel\n    ")])])])},Y=[],q=(n("aef6"),n("75fc")),K=(n("5df3"),n("6762"),[".DS_Store","Thumbs.db"]);function Q(e){return new Promise((function(t){e.file((function(e){return t(e)}))}))}function Z(e){var t=e.createReader();return new Promise((function(e){t.readEntries((function(t){return e(t)}))}))}function ee(e){return te.apply(this,arguments)}function te(){return te=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n,r,a,i,s,o,u,c=arguments;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(n=c.length>1&&void 0!==c[1]?c[1]:"",r=[],!t.isFile||K.includes(t.name)){e.next=10;break}return e.next=5,Q(t);case 5:a=e.sent,i=new File([a],n+t.name,{type:a.type}),r.push(i),e.next=20;break;case 10:if(!t.isDirectory){e.next=20;break}return n+=t.name+"/",e.next=14,Z(t);case 14:return s=e.sent,o=s.map((function(e){return ee(e,n)})),e.next=18,Promise.all(o);case 18:u=e.sent,r.push.apply(r,Object(q["a"])(u));case 20:return e.abrupt("return",r);case 21:case"end":return e.stop()}}),e)}))),te.apply(this,arguments)}function ne(e){return re.apply(this,arguments)}function re(){return re=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n,r,a,i,s,o,u,c,l,f;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:n=[],r=t.dataTransfer.items,a=!0,i=!1,s=void 0,e.prev=5,o=r[Symbol.iterator]();case 7:if(a=(u=o.next()).done){e.next=18;break}if(c=u.value,l=c.webkitGetAsEntry(),!l){e.next=15;break}return e.next=13,ee(l);case 13:f=e.sent,n.push.apply(n,Object(q["a"])(f));case 15:a=!0,e.next=7;break;case 18:e.next=24;break;case 20:e.prev=20,e.t0=e["catch"](5),i=!0,s=e.t0;case 24:e.prev=24,e.prev=25,a||null==o.return||o.return();case 27:if(e.prev=27,!i){e.next=30;break}throw s;case 30:return e.finish(27);case 31:return e.finish(24);case 32:return e.abrupt("return",n.flat(1/0));case 33:case"end":return e.stop()}}),e,null,[[5,20,24,32],[25,,27,31]])}))),re.apply(this,arguments)}var ae=[".pdb",".sdf",".cif",".ppt",".pptx",".odp",".pdf"],ie={props:{path:String},data:function(){return{extensions:ae,showDropzone:!1,isHovering:!1,isUploading:!1,numDropping:0,numEvents:0}},created:function(){document.body.addEventListener("dragenter",this.onDragEnter),document.body.addEventListener("dragleave",this.onDragLeave)},destroyed:function(){document.body.removeEventListener("dragenter",this.onDragEnter),document.body.removeEventListener("dragleave",this.onDragLeave)},methods:{onDragEnter:function(e){this.numEvents++,this.numDropping=e.dataTransfer.items.length,this.showDropzone=!0},onDragLeave:function(e){this.numEvents--,this.numEvents||(this.showDropzone=!1,this.numDropping=0)},onDrop:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return this.isHovering=!1,e.next=3,ne(t);case 3:return n=e.sent,e.next=6,this.upload(n);case 6:this.numDropping=0;case 7:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}(),onChange:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n=t.target.files,e.next=3,this.upload(n);case 3:t.target.value=null,this.numDropping=0;case 5:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}(),upload:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n,r,a,i,s,o,u,c,l,f=this;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:for(this.isUploading=!0,n=[],r=[],a=!0,i=!1,s=void 0,e.prev=6,o=function(){var e=c.value,t=f.extensions.some((function(t){return e.name.endsWith(t)}));t?r.push(e):n.push(e)},u=t[Symbol.iterator]();!(a=(c=u.next()).done);a=!0)o();e.next=15;break;case 11:e.prev=11,e.t0=e["catch"](6),i=!0,s=e.t0;case 15:e.prev=15,e.prev=16,a||null==u.return||u.return();case 18:if(e.prev=18,!i){e.next=21;break}throw s;case 21:return e.finish(18);case 22:return e.finish(15);case 23:if(!r.length){e.next=27;break}return e.next=26,w.upload(this.path,r);case 26:this.$emit("upload");case 27:this.isUploading=!1,this.showDropzone=!1,r.length?n.length&&(l=n.map((function(e){return e.name})).join("\n"),alert("".concat(n.length," unsupported files skipped:\n").concat(l))):alert("No supported files found. Skipping upload.");case 30:case"end":return e.stop()}}),e,this,[[6,11,15,23],[16,,18,22]])})));function t(t){return e.apply(this,arguments)}return t}(),show:function(){this.showDropzone=!0}}},se=ie,oe=(n("1e7f"),Object(u["a"])(se,X,Y,!1,null,null,null)),ue=oe.exports,ce={components:{Breadcrumbs:O,Toolbar:P,FileViewGrid:I,FileViewList:W,FileDropzone:ue},data:function(){return{contextmenu:{show:!1,component:null,path:"",top:0,left:0},displayMode:"grid"}},computed:{path:function(){return this.$route.path}},mounted:function(){this.$root.$on("contextmenu",this.showContextMenu)},destroyed:function(){this.$root.$off("contextmenu",this.showContextMenu)},methods:{refresh:function(){this.$root.$emit("refresh")},showDropzone:function(){this.$refs.dropzone.show()},newFolder:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t){var n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t=t||this.path,n=prompt("Creating folder in ".concat(t,"\nPlease provide a name:"),"new folder"),!n){e.next=6;break}return e.next=5,w.create(t+n);case 5:this.refresh();case 6:this.hideContextMenu();case 7:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}(),deleteItem:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t=this.contextmenu.path,!confirm("Are you sure you want to delete ".concat(t,"?"))){e.next=5;break}return e.next=4,w.delete(t);case 4:this.contextmenu.component?this.contextmenu.component.refresh():this.refresh();case 5:this.hideContextMenu();case 6:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),showContextMenu:function(e){var t=e.event,n=e.path,r=e.component;this.contextmenu.show=!0,this.contextmenu.path=n,this.contextmenu.component=r,this.contextmenu.top=t.pageY+1+"px",this.contextmenu.left=t.pageX+1+"px"},hideContextMenu:function(){this.contextmenu.show=!1}}},le=ce,fe=(n("0117"),Object(u["a"])(le,m,v,!1,null,null,null)),pe=fe.exports,de={components:{FileExplorer:pe},data:function(){return{extensions:ae}}},he=de,me=(n("21bb"),Object(u["a"])(he,d,h,!1,null,null,null)),ve=me.exports;i["a"].use(p["a"]);var xe=new p["a"]({mode:"history",base:"/",routes:[{path:"/*",name:"home",component:ve}]});xe.beforeEach((function(e,t,n){var r=e.path.replace(/\/\/+/g,"/");"/"!==r.slice(-1)&&(r+="/"),r!==e.path&&n({path:r,replace:!0}),n()}));var ge=xe,be=n("ecee"),we=n("c074"),ye=n("ad3d");be["c"].add(we["a"]),i["a"].component("fa-icon",ye["a"]),i["a"].component("fa-layers",ye["b"]),i["a"].component("fa-text",ye["c"]),i["a"].config.productionTip=!1,i["a"].directive("click-out",{bind:function(e,t,n){t.stop=function(e){return e.stopPropagation()},t.event=function(){return n.context[t.expression]()},document.body.addEventListener("click",t.event),e.addEventListener("click",t.stop)},unbind:function(e,t){document.body.removeEventListener("click",t.event),e.removeEventListener("click",t.stop)}}),new i["a"]({router:ge,render:function(e){return e(f)}}).$mount("#app")},"5c0b":function(e,t,n){"use strict";var r=n("e332"),a=n.n(r);a.a},"7a98":function(e,t,n){},"7bf6":function(e,t,n){"use strict";var r=n("5258"),a=n.n(r);a.a},"7fe2":function(e,t,n){},"812f":function(e,t,n){},af21:function(e,t,n){},b751:function(e,t,n){"use strict";var r=n("7fe2"),a=n.n(r);a.a},cf05:function(e,t,n){e.exports=n.p+"img/logo.b8308220.png"},def6:function(e,t,n){},e332:function(e,t,n){},e7ab:function(e,t,n){"use strict";var r=n("af21"),a=n.n(r);a.a},fe45:function(e,t,n){}});
//# sourceMappingURL=app.cc76dda9.js.map
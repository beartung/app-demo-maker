var CP = window.CanvasRenderingContext2D && CanvasRenderingContext2D.prototype;
if (CP && CP.lineTo){
  CP.dashedLine = function(x,y,x2,y2,dashArray){
    if (!dashArray) dashArray=[10,5];
    if (dashLength==0) dashLength = 0.001; // Hack for Safari
    var dashCount = dashArray.length;
    this.moveTo(x, y);
    var dx = (x2-x), dy = (y2-y);
    var slope = dx ? dy/dx : 1e15;
    var distRemaining = Math.sqrt( dx*dx + dy*dy );
    var dashIndex=0, draw=true;
    while (distRemaining>=0.1){
      var dashLength = dashArray[dashIndex++%dashCount];
      if (dashLength > distRemaining) dashLength = distRemaining;
      var xStep = Math.sqrt( dashLength*dashLength / (1 + slope*slope) );
      if (dx<0) xStep = -xStep;
      x += xStep
      y += slope*xStep;
      this[draw ? 'lineTo' : 'moveTo'](x,y);
      distRemaining -= dashLength;
      draw = !draw;
    }
  }
}

/**
 * 实现两点间画箭头的功能
 * @author mapleque@163.com
 * @version 1.0
 * @date 2013.05.23
 */
;(function(window,document){
    if (window.mapleque==undefined)
        window.mapleque={};
    if (window.mapleque.arrow!=undefined)
        return;
    
    /**
     * 组件对外接口
     */
    var proc={
        /**
         * 接收canvas对象，并在此上画箭头（箭头起止点已经设置）
         * @param context
         */
        paint:function(context){paint(this,context);},
        /**
         * 设置箭头起止点
         * @param sp起点
         * @param ep终点
         * @param st强度
         */
        set:function(sp,ep,st){init(this,sp,ep,st);},
        /**
         * 设置箭头外观
         * @param args
         */
        setPara:function(args){
            this.size=args.arrow_size;//箭头大小
            this.sharp=args.arrow_sharp;//箭头锐钝
        }
    };
    
    var init=function(a,sp,ep,st){
        a.sp=sp;//起点
        a.ep=ep;//终点
        a.st=st;//强度
    };
    var paint=function(a,context){
        var sp=a.sp;
        var ep=a.ep;
        if (context==undefined)
            return;
        //画箭头主线
        context.beginPath();
        //context.moveTo(sp.x,sp.y);
        //context.lineTo(ep.x,ep.y);
        context.dashedLine(sp.x, sp.y, ep.x, ep.y, [20, 10]);
        //画箭头头部
        var h=_calcH(a,sp,ep,context);
        context.moveTo(ep.x,ep.y);
        context.lineTo(h.h1.x,h.h1.y);
        context.moveTo(ep.x,ep.y);
        context.lineTo(h.h2.x,h.h2.y);
        context.stroke();
    };
    //计算头部坐标
    var _calcH=function(a,sp,ep,context){
        var theta=Math.atan((ep.x-sp.x)/(ep.y-sp.y));
        var cep=_scrollXOY(ep,-theta);
        var csp=_scrollXOY(sp,-theta);
        var ch1={x:0,y:0};
        var ch2={x:0,y:0};
        var l=cep.y-csp.y;
        ch1.x=cep.x+l*(a.sharp||0.025);
        ch1.y=cep.y-l*(a.size||0.05);
        ch2.x=cep.x-l*(a.sharp||0.025);
        ch2.y=cep.y-l*(a.size||0.05);
        var h1=_scrollXOY(ch1,theta);
        var h2=_scrollXOY(ch2,theta);
        return {
            h1:h1,
            h2:h2
                };
    };
    //旋转坐标
    var _scrollXOY=function(p,theta){
        return {
            x:p.x*Math.cos(theta)+p.y*Math.sin(theta),
            y:p.y*Math.cos(theta)-p.x*Math.sin(theta)
        };
    };
    
    var arrow=new Function();
    arrow.prototype=proc;
    window.mapleque.arrow=arrow;
})(window,document);


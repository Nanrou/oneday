
Page({
  data: {
    today: '几号呢',
    _today: '',
    passed_day: '',
    remain_day: '',

    angle: 0,
    img_src: 'amao6.jpg',

    img_uri: '',
    f_flag: false,
    b_flag: false,
    l_flag: 'hidden',
    msg: '让我看看今天有什么事~'
  },

  handle_success: function(res){
    var ll = res.data.today.split('-')
    this.setData({
      f_flag: true,
      today: ll[1] + '月' + ll[2] + '日',
      _today: res.data.today,
      passed_day: res.data.passed_day,
      remain_day: res.data.remain_day,
      msg: '历史上的今天： ' + res.data.data,
    })
  },

  handle_fail: function(){
    this.setData({
      today: '几号呢',
      f_flag: false,
      msg: '露露和啊毛好像不在喔',
    })
  },

  get_today: function(){
    var that = this
    wx.request({
      url: 'https://oneday.superxiaoshuo.com/oneday/today',
      success: function (res) {
        that.handle_success(res)
      },
      fail: that.handle_fail(),
    })
  },

  onReady: function (){
    this.get_today()
  },

  onPullDownRefresh: function(){
    this.get_today()
    if (this.data.img_src.startsWith('a')){
      this.setData({
        img_src: 'lulu' + Math.floor((Math.random() * 7) + 1)+ '.jpg'
      })
    } else {
      this.setData({
        img_src: 'amao' + Math.floor((Math.random() * 9) + 1) + '.jpg'
      })
    }
    wx.stopPullDownRefresh()
  },

  set_button: function (e){
    this.setData({
      b_flag: !this.data.b_flag,
    })
    switch(this.data.l_flag){
      case '':
        this.setData({
          l_flag: 'hidden',
        })
        break
      case 'hidden':
        this.setData({
          l_flag: '',
        })
        break
    }
  },


  get_thatday: function(event){
    var opt = event.currentTarget.dataset.opt
    this.set_button(event)
    var that = this
    wx.request({
      url: 'https://oneday.superxiaoshuo.com/oneday/' + that.data._today + '/' + opt,
      success: function (res) {
        that.handle_success(res),
        that.set_button(event)
      },
      fail: function(){
        that.handle_fail(),
        that.set_button(event)
      },
    })
    
  },
  rorate_cat: function(){
    switch(this.data.angle){
      case 0:
        this.setData({
          angle: 90,
        })
        break
      case 90:
        this.setData({
          angle: 180,
        })
        break
      case 180:
        this.setData({
          angle: 270,
        })
        break
      case 270:
        this.setData({
          angle: 0,
        })
        break
    }
  }

})
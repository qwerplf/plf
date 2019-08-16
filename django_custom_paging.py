class PageInfo():
 def __init__(self,cur_page,total,per_page=10,show_page=11):
     self.cur_page = cur_page        # 当前页
     self.per_page = per_page        # 一页显示多少行数据
     self.total = total              # 总数据有多少行
     self.show_page = show_page      # 页面显示多少索引

     a,b = divmod(self.total,self.per_page)

     if b:
         a = a + 1
     self.total_page = a         # 总页数


 def get_start(self):
     start = (self.cur_page - 1) * self.per_page
     return start


 def get_end(self):
     return self.cur_page * self.per_page


 def get_page(self):
     half = (self.show_page - 1) // 2

     #### taotal_page = 5 < show_page = 11
     if self.total_page < self.show_page:
         begin = 1
         end = self.total_page
     else:
         #### 左边极值判断
         if self.cur_page - half <= 0:
             begin = 1
             # end = self.cur_page + half
             end = self.show_page
         #### 右边极值的判断
         elif self.cur_page + half > self.total_page:
             # begin =  self.cur_page - half
             begin = self.total_page - self.show_page + 1
             end = self.total_page  ### 31
         #### 正常页码判断
         else:
             begin = self.cur_page - half
             end = self.cur_page + half

     page_list = []
     if self.cur_page == 1:
         astr = "<li><a href='#' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a></li>"
     else:
         astr = "<li><a href='/test3/?cur_page=%s' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a></li>" % (
                     self.cur_page - 1)
     page_list.append(astr)

     for i in range(begin, end + 1):
         if self.cur_page == i:
             # astr = "<a style='display:inline-block; padding:5px;margin:5px;background-color:red;' href='/custom/?cur_page=%s'>%s</a>" % (i, i)
             astr = "<li class='active'><a href='/test3/?cur_page=%s'>%s</a></li>" % (i, i)
         else:
             # astr = "<a style='display:inline-block; padding:5px;margin:5px' href='/custom/?cur_page=%s'>%s</a>" % (i, i)
             astr = "<li><a href='/test3/?cur_page=%s'>%s</a></li>" % (i, i)
         page_list.append(astr)

     if self.cur_page == self.total_page:
         astr = "<li><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>"
     else:
         astr = "<li><a href='/test3/?cur_page=%s' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>" % (
                     self.cur_page + 1)
     page_list.append(astr)

     s = " ".join(page_list)

     return s






def test3(request):

 # mysql中limit的分页公式
 '''
 cur_page:   当前页
 show_page_num：   显示多少页
 start_page：     起始页

 limit 起始位置a, 显示多少页b
 a = ( cur_page - 1 ) * show_page_num
 b = show_page_num
 '''


 # 在django中的分页公式（models.UserInfo.objects.filter(id__lte=44)[start:end]）
 """
 show_page_num = 10
 cur_page = 1   start = 0   end = 10
 cur_page = 2   start = 10  end = 20
 cur_page = 3   start  =20  end = 30
 
 start = (cur_page - 1) * show_page_num
 end = cur_page * show_page_num
 """
 cur_page = request.GET.get("cur_page")
 cur_page = int(cur_page)

 total = models.UserInfo.objects.count()

 obj = PageInfo(cur_page,total)

 start = obj.get_start()
 end = obj.get_end()

 # 获取总数据
 user_list = models.UserInfo.objects.all()[start:end]

 return render(request,'custom.html',{"user_list":user_list,"page":obj})

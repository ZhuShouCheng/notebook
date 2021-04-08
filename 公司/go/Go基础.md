# Go语言圣经

#### 入门

1. Go语言不需要在语句或者声明的末尾添加分号，除非一行上有多条语句

2. 和大多数编程语言类似，区间索引时，Go言里也采用左闭右开形式

3. 自增语句`i++`给`i`加1；这和`i += 1`以及`i = i + 1`都是等价的，它们是语句，而不像C系的其它语言那样是表达式

4. `range`产生一对值；索引以及在该索引处的元素值

5. `空标识符`，即`_`可用于在任何语法需要变量名但程序逻辑不需要的时候（如：在循环里）丢弃不需要的循环索引，并保留元素值

6. ```go
   counts := make(map[string]int)	//创建一个map
   ```

7. 复合声明

   ```go
   var palette = []color.Color{color.White, color.Black} //动态数组
   ```

   ```go
   anim := gif.GIF{LoopCount: nframes}
   //      数据类型(struct)  变量赋值   
   ```

8. 并发执行

   goroutine是一种函数的并发执行方式，而channel是用来在goroutine之间进行参数传递

   ```go
   ch := make(chan string) //channel 
       for _, url := range os.Args[1:] {
           go fetch(url, ch) // start a goroutine
       }
   ```

   当一个goroutine尝试在一个channel上做send或者receive操作时，这个goroutine会阻塞在调用处
   
   -----

9. ：=运算符是一种用于在一行中声明和初始化变量的快捷方式（Go使用右侧的值来确定变量的类型）。
10. 函数首字母大写表示可以被外部文件访问，小写表示该函数仅在包内使用
11. nil = null 用于error ?
12. log.Fatal 用于输出error信息，并停止项目

13. slice 切片 相当于动态数组

14. 测试命令可以执行以_test结尾的测试文件中的Test开头的函数



---------------

15. map参数传递时的写法 map[string]string







设置镜像仓库

```text
1. 右键 我的电脑 -> 属性 -> 高级系统设置 -> 环境变量
2. 在 “[你的用户名]的用户变量” 中点击 ”新建“ 按钮
3. 在 “变量名” 输入框并新增 “GOPROXY”
4. 在对应的 “变量值” 输入框中新增 “https://goproxy.io,direct”
5. 最后点击 “确定” 按钮保存设置
```
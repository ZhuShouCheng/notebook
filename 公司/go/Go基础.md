# Go语言圣经

#### 安装

设置镜像仓库

```text
1. 右键 我的电脑 -> 属性 -> 高级系统设置 -> 环境变量
2. 在 “[你的用户名]的用户变量” 中点击 ”新建“ 按钮
3. 在 “变量名” 输入框并新增 “GOPROXY”
4. 在对应的 “变量值” 输入框中新增 “https://goproxy.io,direct”
5. 最后点击 “确定” 按钮保存设置
```

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



## 数据类型

#### string

```Go
func Replace(s, old, new string, n int) string
```

返回将s中前n个不重叠old子串都替换为new的新字符串，如果n<0会替换所有old子串。

```go
func Split(s, sep string) []string
```

用去掉s中出现的sep的方式进行分割，会分割到结尾，并返回生成的所有片段组成的切片（每一个sep都会进行一次切割，即使两个sep相邻，也会进行两次切割）。如果sep为空字符，Split会将s切分成每一个unicode码值一个字符串。



#### slice 

声明方式：var identifier []type

slice 不能使用==进行比较，不过可以使用bytes.Equal函数来判断字节形slice

对于其他元素的slice，需要我们自行实现equal函数

```Go
runes = append(runes, r)
```

由于不能确定append调用是否导致了内存的重新分配，因此也不能确定新的slice和原始的slice是否使用相同的底层数组空间。因此，通常将append返回的结果直接赋值给输入的slice变量

```Go
x = append(x, x...) // append the slice x
```

​	append 添加切片的方式

```Go
for _, name := range names {
   
}
```

range names返回两个值	slice的索引值以及当前索引的元素

#### Map

Map的迭代顺序是不确定的，如果要按顺序遍历key/value对，我们必须显式地对key进行排序

方法：1.将key取出放入slice	2.对slice进行排序	3.按slice顺序取Map

Map必须使用前必须进行初始化



#### Struct

##### 匿名成员

Go语言有一个特性让我们只声明一个成员对应的数据类型而不指名成员的名字；这类成员就叫匿名成员

得益于匿名嵌入的特性，我们可以直接访问叶子属性而不需要给出完整的路径。

实际上，外层结构体不仅仅获得了匿名成员类型的所有成员，也获得了该类型导出的全部方法



## 函数

#### 递归

```Go
func outline(stack []string, n *html.Node) {
    if n.Type == html.ElementNode {
        stack = append(stack, n.Data) // push tag
        fmt.Println(stack)
    }
    for c := n.FirstChild; c != nil; c = c.NextSibling {
        outline(stack, c)
    }
}
```





## IO



```Go
bufio.NewReader(file).ReadLine()
```

读取文件一行






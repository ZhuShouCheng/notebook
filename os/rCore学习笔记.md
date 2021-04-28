# Lab1：Booting a PC

## Part 1: PC Bootstrap

#### x86汇编

##### AT&T语法

mov ebx,eax	操作数在左，目标数在右

立即数前面加"$"，寄存器前面加"%"

cmpl指令将两个操作数相减，但计算结果并不保存，只是根据计算结果改变eflags寄存器中的标志位，如果两个操作数相等，则计算结果为0，eflags中的ZF位置1。

jne	条件转移指令(jump not equal) ZF=0，则进行跳转

xor	异或指令

cmp	比较两操作数大小

sub	不带借位的减法指令

CLI：Clear Interupt，禁止中断发生。STL：Set Interupt，允许中断发生。CLI和STI是用来屏蔽中断和恢复中断用的，如设置栈基址SS和偏移地址SP时，需要CLI，因为如果这两条指令被分开了，那么很有可能SS被修改了，但由于中断，而代码跳去其它地方执行了，SP还没来得及修改，就有可能出错。
CLD: Clear Director。STD：Set Director。在字行块传送时使用的，它们决定了块传送的方向。CLD使得传送方向从低地址到高地址，而STD则相反。

LIDT: 加载中断描述符。LGDT：加载全局描述符。

leave	指令将EBP寄存器的内容复制到ESP寄存器中，以释放分配给该过程的所有堆栈空间。然后，它从堆栈恢复EBP寄存器的旧值

ret	子程序结束时使用，将返回函数调用的下一个指令

CALL	跳转，并且将下一条指令入栈

##### 寄存器

ESP寄存器	系统&用户栈顶指针

EBP寄存器	用户栈底指针



-------------------------

#### 物理地址空间

```
+------------------+  <- 0xFFFFFFFF (4GB)
|      32-bit      |
|  memory mapped   |
|     devices      |
|                  |
/\/\/\/\/\/\/\/\/\/\

/\/\/\/\/\/\/\/\/\/\
|                  |
|      Unused      |
|                  |
+------------------+  <- depends on amount of RAM
|                  |
|                  |
| Extended Memory  |
|                  |
|                  |
+------------------+  <- 0x00100000 (1MB)
|     BIOS ROM     |
+------------------+  <- 0x000F0000 (960KB)
|  16-bit devices, |
|  expansion ROMs  |
+------------------+  <- 0x000C0000 (768KB)
|   VGA Display    |
+------------------+  <- 0x000A0000 (640KB)
|                  |
|    Low Memory    |
|                  |
+------------------+  <- 0x00000000
```

Low Memory ???	早期计算机使用？

BIOS	完成机器自检，对系统进行初始化，如加载显卡和检查内存总量，执行完初始化操作后，将从适当的位置加载操作系统，并将计算机的控制权传递给操作系统。早期的BIOS写在ROM（只读存储器）中，但当前PC将BIOS存储在闪存中。

Low 1MB	现代PC保留了原始布局，用于向后兼容，如286在实模式下运行。（最初的IBM PC中的Intel 8088 CPU能够寻址1MB，故称为1MB障碍。后来的Intel 80286和80386打破了1MB障碍）

#### The ROM BIOS

CS	代码段寄存器

IP	指令寄存器

``` 
[f000:fff0] 0xffff0:	ljmp   $0xf000,$0xe05b
  CS   IP
```

由于PC中的BIOS是“硬连线”到物理地址范围0x000f0000-0x000fffff，因此该设计可确保BIOS始终在上电或任何系统重新启动后始终首先获得对计算机的控制-这是至关重要的，因为在通电时， 机器的RAM中没有其他软件可以执行的软件。

在实模式中，物理地址= 16 * 端地址 + 偏移量

```
 16 * 0xf000 + 0xfff0  = 0xf0000 + 0xfff0 = 0xffff0 
```





## Part 2:The Boot Loader

PC上的软盘和硬盘被分为512字节区域，称为扇区

如果磁盘可引导，则第一个扇区被称为引导扇区，引导加载程序代码所在

JOS 的引导由`boot/boot.S`的汇编程序和`boot/main.c`的C程序两个程序完成

#### boot.S

主要是将处理器从实模式转换到 32 位的保护模式

1. 初始化常用寄存器
2. 打开A20地址线，让程序可以访问1MB以上的内存地址
3. 加载全局描述符表，打开保护模式
4. 执行bootmain函数

##### bootmain.c

读取第一个扇区，运行内核

##### GDB命令

- ctrl-c 中止当前程序运行，进入gdb
- c 继续运行到断点位置
- si 执行一条指令
- b function/b file:line 在function处设置断点
- b *addr 在某地址处设置断点
- x/ni 显示接下来n条指令  x/nx add显示接下来n个16进制 +add 用来打印add地址中存储的数据
- i r 显示寄存器中的内容
- clear *address    删除断点（应该和b的语法一致）
- help  含全部指令信息

----------

#### ELF文件结构

在Blackfin的Linux世界中，有两种基本的文件格式：

- FLAT：二进制的Flat文件通常被称为BFLT，它是基于原始的a.out格式的一种相对简单的轻量级可执行格式。BFLT文件是嵌入式Linux的默认文件格式。
- FDPIC ELF(The Executable and Linking Format)：可执行和可链接格式最初是由Unix System实验室开发出来的，现在已经成为文件格式的标准。相对于BFLT格式而言，ELF标准更强大并且更灵活。但是，它更重量级一些，需要更多的磁盘空间以及有一定的运行时开销。

这两种格式都支持静态和动态链接（共享库），但是，ELF更容易使用及创建动态链接库。只有ELF支持动态加载（dlopen(), dlsym(), dlclose()），以及创建和维护共享库的标准方法。

##### EFI结构

ELF文件格式提供了两种视图，分别是链接视图和执行视图

链接视图是以节（section）为单位，执行视图是以段（segment）为单位

![EFI结构](pic\EFI结构.png)



``` c
// ELF 文件头	描述程序头表项以及其他内容
struct Elf {
    uint32_t e_magic; // 标识是否是ELF文件
    uint32_t e_entry; // 程序入口点
    uint32_t e_phoff; // 程序头表偏移值
    uint16_t e_phnum; // 程序头部个数
};
//程序头表项		描述section内容?
struct Proghdr { 
    uint32_t p_offset; // 段位置相对于文件开始处的偏移量
    uint32_t p_pa; // 段的物理地址
    uint32_t p_memsz; // 段在内存中的长度 
}
```

链接地址与物理地址 ？？？ Execrise 5  为什么在ljump出错？

[ELF详细资料](https://blog.csdn.net/mergerly/article/details/94585901)



## Part 3: The Kernel

#### 虚拟内存解决位置依赖

操作系统内核一般期望加载到高位地址，希望将低位地址留给用户

因此将虚拟地址0xf0100000（内核的链接地址）映射为物理地址0x00100000

内核映射虚拟地址 [KERNBASE, KERNBASE+4MB) 到物理地址 [0, 4MB)，并开启分页功能使得映射得到执行（足够早期的使用）

#### 标准化输入到控制台

#define va_start(ap, last) __builtin_va_start(ap, last)	编译器内置函数

可变参数的宏实现

va_start(ap, last)	last后面一个参数即为可变参数列表

va_arg(ap, type)	以type类型读取可变参数列表中一个参数

va_end(ap)	将指针释放，防止野指针

putch是输出函数，它调用了cputchar函数，最终cputchar调用了cga_putc函数来完成显示功能

在cga_putc函数中的crt_buf 是一个指向 16 位无符号整形数的静态指针，它实际上指向的是内存中物理地址为 0xb8000 的位置，在前面章节我们已经知道物理内存的 0xa0000 到 0xc0000 这 128KB 的空间是留给 VGA 显示缓存。在JOS中，显示屏规定为 25 行，每行可以输出 80 个字符，由于每个字符实际上占显存中的两个字节(字符ASCII码和字符属性)，于是物理内存中从 0xb8000 到 0xb8fa0 之间的内容都可以用字符的形式在屏幕上显示出来。

这部分涉及了大量代码，但大概思路并不难理解。不过console.c中包含了in out，其中的一些地址、操作意义不是很清楚

#### 栈

系统栈的起始地址在entry.S中定义，为0xf010000，栈从高位往低位扩展

esp寄存器存储栈顶指针，ebp寄存器存储系统栈最上面栈帧的栈底指针

call调用存储的下一条指令地址 = 上一个栈帧栈底指针 + 1

调用的函数参数	ebp+2 依次往上，不过无法确定个数

ebp存储的是上一个栈底指针的地址

![image-20210426145852530](D:\笔记\notebook\os\pic\栈结构.png)

execrise 12不想做	等有空再补吧

-----

# Lab2：Memory Management

#### git命令

git pull	命令用于从远程获取代码并合并本地的版本。 

git pull origin master:brantest 将远程主机 origin 的 master 分支拉取过来，与本地的 brantest 分支合并。

git checkout	命令用于创建或切换分支。

git checkout -b lab2 origin/lab2 首先创建一个基于origin/lab2的本地分支lab2，其次改变lab文件夹的内容以映射储存在lab2分支的文件。

git checkout *branch-name* 切换分支

## Part 1: Physical Page Management

MMU：内存管理单元，主要实现虚拟地址到物理地址的转换


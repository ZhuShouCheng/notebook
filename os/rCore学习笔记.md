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

git fetch	获取远程库的最新代码

git checkout	命令用于创建或切换分支。

git checkout -b lab2 origin/lab2 首先创建一个基于origin/lab2的本地分支lab2，其次改变lab文件夹的内容以映射储存在lab2分支的文件。

git checkout *branch-name* 切换分支

git reset --hard	放弃本地修改



## Part 1: Physical Page Management

MMU：内存管理单元，主要实现虚拟地址到物理地址的转换







--------

## Lec 01 Introduction and Example

#### fork

fork会拷贝当前进程的内存，并创建一个新的进程，这里的内存包含了进程的指令和数据。之后，我们就有了两个拥有完全一样内存的进程。fork系统调用在两个进程中都会返回，在原始的进程中，fork系统调用会返回大于0的整数，这个是新创建进程的ID。而在新创建的进程中，fork系统调用会返回0。所以即使两个进程的内存是完全一样的，我们还是可以通过fork的返回值区分旧进程和新进程。

某种程度上来说这里的拷贝操作浪费了，因为所有拷贝的内存都被丢弃并被exec替换。在大型程序中这里的影响会比较明显。实际上操作系统会对其进行优化。

fork创建的新进程从fork语句后开始执行，因为新进程也继承了父进程的PC程序计数器。新进程继承的是父进程执行到fork语句时的状态。

xv6中唯一不是通过fork创建进程的场景就是创建第一个进程的时候，这时需要设置程序计数器为0。

#### exec

代码会执行exec系统调用，这个系统调用会从指定的文件中读取并加载指令，并替代当前调用进程的指令。从某种程度上来说，这样相当于丢弃了调用进程的内存，并开始执行新加载的指令。

- exec系统调用会保留当前的文件描述符表单。所以任何在exec系统调用之前的文件描述符，例如0，1，2等。它们在新的程序中表示相同的东西。

- 通常来说exec系统调用不会返回，因为exec会完全替换当前进程的内存，相当于当前进程不复存在了，所以exec系统调用已经没有地方能返回了。

在运行shell时，我们不希望系统调用替代了Shell进程，实际上，Shell会执行fork，这是一个非常常见的Unix程序调用风格。对于那些想要运行程序，但是还希望能拿回控制权的场景，可以先执行fork系统调用，然后在子进程中调用exec。

#### pipe

管道是一个小的内核缓冲区，它以文件描述符对的形式提供给进程，一个用于写操作，一个用于读操作。从管道的一端写的数据可以从管道的另一端读取。管道提供了一种进程间交互的方式。

```c
int p[2];
pipe(p);
p[0];	//读操作fd
p[1];	//写操作fd
```

---------

## Lec03 OS Organization and System Calls 

操作系统必须满足三个要求：多路复用，隔离和交互。 

#### 指令级别

机器模式、特权模式、用户模式

机器模式只在开机时使用

#### 内核组织方式

##### monolithic kernel（宏内核）

整个操作系统全部在内核中。

优点：结构简单、便于不同部分协作（可以共享cache），性能较好

缺点：不同部分之间的接口代码复杂，一旦某部分出现错误，整个内核将崩溃

##### microkernel（微内核）

将尽可能少的操作系统代码运行于特权态，大部分代码执行在用户态

#### 进程

进程包含页表、用户栈、内核栈

页表用来记录进程的虚拟地址空间

进程运行在用户态时使用用户栈，使用系统调用切换到特权态时使用内核栈。用户态无法写内核栈，特权态时，用户栈也无法使用

#### 硬件实现强隔离

硬件对于强隔离的支持包括了：user/kernle mode和虚拟内存

user/kernel mode：特殊权限指令主要是一些直接操纵硬件的指令和设置保护的指令，例如设置page table寄存器、关闭时钟中断。在处理器上有各种各样的状态，操作系统会使用这些状态，但是只能通过特殊权限指令来变更这些状态。

虚拟内存：处理器包含了page table，而page table将虚拟内存地址与物理内存地址做了对应。

#### 模式切换

用户的应用程序执行系统调用的唯一方法就是调用ECALL指令，并将对应的数字作为参数传给ECALL。之后再通过ECALL跳转到内核。

#### 系统调用流程

在RISC-V中，有一个专门的指令用来实现这个功能，叫做ECALL。ECALL接收一个数字参数，当一个用户程序想要将程序执行的控制权转移到内核，它只需要执行ECALL指令，并传入一个数字。这里的数字参数代表了应用程序想要调用的System Call。

每一个从应用程序发起的系统调用都会调用到syscall函数，syscall函数会检查ECALL的参数，通过函数数组的方式运行系统调用





## Lec04 Page tables

#### 分页硬件

页表是由页表项（PTE）组成的数组。PTE中包含了物理页码（PPN）以及一些标志，来控制物理空间块的读写访问权限。

物理地址与虚拟地址的映射为三层树形结构，每一层存储下一层页表页的地址，最后一层存储物理地址的PTE。

> 页表所涉及的是内存地址问题，不要模糊内存与磁盘。

![image-20210523212749086](D:\笔记\notebook\os\pic\物理地址和虚拟地址映射.png)



#### 页表

虚拟内存实现隔离，每个进程有属于自己的地址空间，因而无法修改其他进程和内核的内存

实现地址空间最常见的办法是页表。

页表是在硬件中通过处理器和内存管理单元（MMU）实现。

对于任何带有地址的指令，其中的地址应被认为是虚拟内存地址而不是物理地址。一旦MMU打开，所有指令地址都是虚拟内存地址。

##### SATP寄存器

MMU存储着物理内存与虚拟内存映射表单，该表单地址放在SATP的寄存器中。当CPU从一个程序切换到另一个程序中时，同时也需要切换SATP寄存器中的内容。

##### 三级结构

虚拟地址到物理地址的转换（VA to PA）

翻译方式：index + offset	

39bit	27bit用于index	12bit用于offset，对应4096个字节

##### 标志位

第一个标志位是Valid。如果Valid bit位为1，那么表明这是一条合法的PTE，

下两个标志位分别是Readable和Writable。表明你是否可以读/写这个page。

Executable表明你可以从这个page执行指令。

User表明这个page可以被运行在用户空间的进程访问。

![img](https://gblobscdn.gitbook.com/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MKQ3oLlaUanoFBXrOu6%2F-MKVD5xKfkcui0853IM6%2Fimage.png?alt=media&token=d4198af2-e6ac-4af4-b1b2-cf600a7bebd1)



#### 页表缓存TLB

翻译虚拟地址需要读三次内存，代价太高，因此通常会使用缓存 Translation Lookside Buffer即页表内存（TLB）

#### 内核页表

为了性能要求，内核页表中虚拟地址与物理地址相同。

The kernel configures the layout of its ad-dress space to give itself access to physical memory and various hardware resources at predictablevirtual addresses. 	？不太明白

**问题1：为什么内核空间页表各进程内容是完全一样，还需要每个进程独立一份**
我认为是出于性考虑，如果所有进程在内核态都使用同一份页表，CPU从用户态进入内核态的所有场景（系统调用，硬中断），首先做的一个事情就是切页表，然后得刷TLB等事情，开销较大，不可接受，所以采用每个进程进入内核态进不需要切换页表的方案。

##### 每个进程都有一份内核栈？

内核栈就是用来纪录进程内核态的执行状态的。每个进程都维护着自己的内核栈，栈中保存着进程在内核态时各寄存器等的值。



#### Lab

(pte & PTE_V) == 0	指pte的vflag为0还是为1？

pte & (PTE_R|PTE_W|PTE_X)  |代表什么意思，或 还是 且

vm.c是模拟硬件实现吗？实际上这部分应该由硬件实现？







## Lec05 Calling conventions and stack frames RISC-V

#### 名词解释

RISC-V	基于精简指令集（RISC）原则的开源指令集架构（ISA）。

x86通常被称为复杂指令集(CISC)

ARM(Advanced RISC Machine)	第一款基于RISC的微处理器

#### RISC 寄存器

![img](https://gblobscdn.gitbook.com/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MM-XjiGboAFe-3YvZfT%2F-MM0rYc4eVnR9nOesAAv%2Fimage.png?alt=media&token=f30ebac8-8dc0-4b5d-8aa7-b241a10b43b3)

- Caller Saved寄存器在函数调用的时候不会保存

- Callee Saved寄存器在函数调用的时候会保存

#### 栈

##### stack frame（栈帧）

每一次我们调用一个函数，函数都会为自己创建一个Stack Frame，并且只给自己用。函数通过移动Stack Pointer来完成Stack Frame的空间分配。

<img src="https://gblobscdn.gitbook.com/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MM3Hk7Gv6ibvM2lxjCc%2F-MM4D2J3t3ajqkngxRPC%2Fimage.png?alt=media&token=1f78ffd1-9322-4666-85f2-8aa831ced49e" alt="img" style="zoom:67%;" />

##### 汇编函数

组成

1. Function prologue（函数序言）
2. Body（函数主体）
3. Epollgue（函数尾声）

## Lec06 Isolation & system call entry/exit

用户空间和内核空间之间的切换通常称为trap

#### trap机制

##### trap的三种形式

1. 系统调用引发
2. 异常发生
3. 设备中断

##### trap的保存流程

1. 首先，我们需要保存32个用户寄存器。因为很显然我们需要恢复用户应用程序的执行，尤其是当用户程序随机的被设备中断所打断时。

2. 程序计数器也需要在某个地方保存，它几乎跟一个用户寄存器的地位是一样的，我们需要能够在用户程序运行中断的位置继续执行用户程序。

3. 我们需要将mode改成supervisor mode，因为我们想要使用内核中的各种各样的特权指令。

4. SATP寄存器现在正指向user page table，而user page table只包含了用户程序所需要的内存映射和一两个其他的映射，它并没有包含整个内核数据的内存映射。所以在运行内核代码之前，我们需要将SATP指向kernel page table。

5. 我们需要将堆栈寄存器指向位于内核的一个地址，因为我们需要一个堆栈来调用内核的C函数。

6. 一旦我们设置好了，并且所有的硬件状态都适合在内核中使用， 我们需要跳入内核的C代码。

##### supervise mode权限

其中的一件事情是，你现在可以读写控制寄存器了。比如说，当你在supervisor mode时，你可以：读写SATP寄存器，也就是page table的指针；STVEC，也就是处理trap的内核指令地址；SEPC，保存当发生trap时的程序计数器；SSCRATCH等等。在supervisor mode你可以读写这些寄存器，而用户代码不能做这样的操作。

另一件事情supervisor mode可以做的是，它可以使用PTE_U标志位为0的PTE。当PTE_U标志位为1的时候，表明用户代码可以使用这个页表；如果这个标志位为0，则只有supervisor mode可以使用这个页表。

#### 用户空间trap

Trap Frame是指中断、自陷、异常进入内核后，在堆栈上形成的一种数据结构

##### ecall指令

第一，ecall将代码从user mode改到supervisor mode

第二，ecall将程序计数器的值保存在了SEPC寄存器。

第三，ecall会跳转到STVEC寄存器指向的指令

##### 代码描述	usertrap

之所以叫trampoline page，是因为你某种程度在它上面“弹跳”了一下，然后从用户空间走到了内核空间。

首先，ecall指令跳转到STVEC寄存器指向的地址，即trampoline.S中的uservec

首先获得Trap Frame的地址，将寄存器的值写入到Frame中，恢复内核栈栈顶指针（即切换到内核栈），恢复satp（Supervisor Address Translation and Protection Register）寄存器的内容（包含了指向page table的物理地址），最后调用trap.c中的usertrap函数	

usertrap函数先切换到内核态，将kernelvec地址写入到stvec寄存器（设置内核中断的处理方式）中，保存用户程序计数器值，开启中断，根据scause寄存器的值判断异常原因，处理异常，系统调用则调用syscall()函数，如果是设备中断，则执行中断，如果是出现异常，则打印并关闭进程。最后如果是时间中断，则放弃CPU之后调用usertrapret函数（复原函数）。	

usertrapret函数执行相反的操作，将内核态下的寄存器进行保存，这样下一次从用户空间转换到内核空间时可以用到这些数据，切换到用户态，调用userret，userret将satp切换到用户页表，读取Trap Frame中保存的寄存器值。

##### 为什么trampoline page要求用户空间和内核空间映射地址相同？

trampoline page在user page table中的映射与kernel page table中的映射是完全一样的。这两个page table中其他所有的映射都是不同的，只有trampoline page的映射是一样的，因此我们在切换page table时，寻址的结果不会改变，我们实际上就可以继续在同一个代码序列中执行程序而不崩溃。这是trampoline page的特殊之处，它同时在user page table和kernel page table都有相同的映射关系。



##### 系统调用的返回值问题

RISC-V上的C代码的习惯是函数的返回值存储于寄存器a0，所以为了模拟函数的返回，我们将返回值存储在trapframe的a0中。之后，当我们返回到用户空间，trapframe中的a0槽位的数值会写到实际的a0寄存器，Shell会认为a0寄存器中的数值是write系统调用的返回值。

##### 代码描述	exec

何时被调用？

首先将exec调用的参数放入a0、a1，将系统调用的编码放到a7，然后执行ecall指令。

ecall指令将陷入（翻译不达意）到内核中，执行uservec，usertrap，以及syscall。

当系统调用结束，syscall将结果记录在p->trapframe->a0中

PGROUNDDOWN	宏，用来将地址对齐到4K，便于进行页表操作

#### 内核空间trap

可处理中断：设备中断、发生异常

代码流程相当于用户空间trap的简化版，因为从内核发起的话，程序已经在使用kernel page table。所以当trap发生时，程序执行仍然在内核的话，很多处理都不必存在。

#### Lab

定时器到时间时，调用定义过的函数

该函数位于用户地址空间中，没法直接在内核中调用，所以只能将trapframe中程序计数器指向该函数

如果自己调，可能要调好久也不一定能找出来，有点挫败感

##### 函数指针

如果在程序中定义了一个函数，那么在编译时系统就会为这个函数代码分配一段存储空间，这段存储空间的首地址称为这个函数的地址。而且函数名表示的就是这个地址。既然是地址我们就可以定义一个指针变量来存放，这个指针变量就叫作函数指针变量，简称函数指针。



## Lec08 Page faults

page fault可以让内存地址映射关系变得动态起来。通过page fault，内核可以更新page table，这是一个非常强大的功能。因为现在可以动态的更新虚拟地址这一层抽象，结合page table和page fault，内核将会有巨大的灵活性。

#### COW（copy on write）

写拷贝是一种可以推迟甚至是免除拷贝数据的技术。子进程、父进程只读性的共享所有物理块，当进程执行写入指令时，系统提起缺页异常，内核将对缺页的页进行复制，分别映射。

资源的复制只有在需要写入的时候才进行，在此之前，只是以只读方式共享。

#### Lazy allocation

在程序调用sbrk扩充heap段空间时，仅仅分配虚拟空间，并且标记该地址在页表中不合法（没分配物理空间）

当新的地址出现缺页异常时，内核才分配物理空间并映射到页表中

#### Zero Fill On Demand

某些程序载入时包含了大量0填充的页面，比如bss段中的一个大型零矩阵，可以将这个部分占用的页面映射成一个只读的0页面，当需要用到时，内核将重新分配一个0page供程序使用。

#### Demand Paging

当需要使用某一程序时，再将其装入到内存中

首先，在虚拟地址空间中，为text和data分配好地址段，但其相应的PTE不对应任何物理内存page

当需要用到该程序时，将从text段中最开始位置触发page fault，这些page的类型是on-demand page

#### Memory Mapped Files

关于文件映射到内存的问题

在内存中，加载文件是已lazy的方式实现的，你不会立即将文件内容拷贝到内存中，而是先记录这个PTE属于这个文件描述符，只有当真正用到是才会真正将文件加载进来。

在将文件写回时，PTE中dirty bit记录了是否被修改过，只需将dirty bit为1的页写回到文件中。

#### Lab

##### 相关寄存器 

SCAUSE	保存了trap机制中进入到supervisor mode的原因，13表示因load引起的page fault，15表示因store引起的page fault，12表示因指令引起的page fault（错误类型）

STVAL	出现page fault（or 出现任何错误）的虚拟地址（内存地址）

SEPC	触发page fault的指令地址（代码地址）



## Lec09 Interrupts

##### 代码描述	Console input

首先，内核main函数调用consoleinit实现对UART硬件的初始化，主要是写寄存器来控制硬件的工作模式

shell调用open方法获取控制台，通过read系统调用来调用consoleread

consoleread等待硬件中断将数据放入到buf，之后将buf中的数据写入到用户空间中，并且对一些特殊字符进行处理

每当用户输入字符时，UART将产生一个中断，中断处理程序使用devintr获得中断类型，然后调用uartintr处理中断。

uartintr从寄存器中获取一个字符，然后调用consoleintr处理字符

consoleintr将字符写入到buf中，并且在一行结束时唤醒consoleread

#### Interrupt硬件概述

中断与系统调用的区别：

1. 异步
2. 并发
3. program device(这些设备需要被编程)

硬件设备会映射到内核内存地址的某处，类似于读写内存，内核通过向相应的设备地址执行load/store指令来对设备进行编程

所有外部设备都连接到处理器上，CPU通过PLIC（Platform Level Interrupt Control）来管理设备中断

处理流程：

- PLIC会通知当前有一个待处理的中断

- 其中一个CPU核会Claim接收中断，这样PLIC就不会把中断发给其他的CPU处理

- CPU核处理完中断之后，CPU会通知PLIC

- PLIC将不再保存中断的信息

#### 设备驱动架构

驱动一般分为两个部分，bottom/top

bottom部分通常是Interrupt handler。当一个中断送到了CPU，并且CPU设置接收这个中断，CPU会调用相应的Interrupt handler。Interrupt handler并不运行在任何特定进程的context中，它只是处理中断。

top部分，是用户进程，或者内核的其他部分调用的接口。对于UART来说，这里有read/write接口，这些接口可以被更高层级的代码调用。

通常情况下，驱动中会有一些队列（或者说buffer），top部分的代码会从队列中读写数据，而Interrupt handler（bottom部分）同时也会向队列中读写数据。这里的队列可以将并行运行的设备和CPU解耦开来。

#### 设备中断发生

场景：在按下键盘后，触发一个中断

假设键盘生成了一个中断并且发向了PLIC，PLIC会将中断路由给一个特定的CPU核，并且如果这个CPU核设置了SIE寄存器的E bit（注，针对外部中断的bit位），那么会发生以下事情：

- 首先，会清除SIE寄存器相应的bit，这样可以阻止CPU核被其他中断打扰，该CPU核可以专心处理当前中断。处理完成之后，可以再次恢复SIE寄存器相应的bit。
- 之后，会设置SEPC寄存器为当前的程序计数器。我们假设Shell正在用户空间运行，突然来了一个中断，那么当前Shell的程序计数器会被保存。
- 之后，要保存当前的mode。在我们的例子里面，因为当前运行的是Shell程序，所以会记录user mode。
- 再将mode设置为Supervisor mode。
- 最后将程序计数器的值设置成STVEC的值。（注，STVEC用来保存trap处理程序的地址）在XV6中，STVEC保存的要么是uservec或者kernelvec函数的地址，具体取决于发生中断时程序运行是在用户空间还是内核空间。



#### 代码流程

##### 初始化

在bootloader结束后调用start.c，初始化中断寄存器

main函数执行设备初始化程序

uartinit通过写寄存器的方式，将uart设备配置成正常模式

main函数中还将调用PLIC初始化程序

plicinit中以写设备的方式开启设备的中断，并使用plicinithart给CPU设置所处理的中断类型

最后开启SSTATUS中断寄存器接受中断

##### 驱动程序top部分（通过接口，操作设备）

首先讨论shell程序向console打印一个“$”的过程

shell使用write系统调用向console写入一个“$”

进入系统调用中断，处理write的系统调用sys_write使用了内核的filewrite函数

filewrite函数首先判断写入的文件是否为设备，然后调用相应设备的write接口，这里即consolewrite函数

consolewrite借助either_copyin将字符串“$”从用户页表中读出（具体上，在用户空间调用write时，就将字符串的地址传递进去了，到了内核后，通过访问用户页表的该虚拟地址，将字符串读取），之后调用uartputc将字符串写入到设备中

uartputc负责向设备维护的一个环形队列写入内容（通过两个控制指针），而后调用uartstart函数，该函数会将队列中全部内容写入到设备中，并唤醒读取函数，一旦数据送到设备，系统调用会返回。

##### 驱动程序的bottom部分（中断处理）

？？？到底在处理啥中断？？？

假设用户通过键盘输入了“l”，这会导致“l”被发送到主板上的UART芯片，产生中断之后再被PLIC路由到某个CPU核

和正常中断类似，保存相应寄存器后，进入trap后，执行devintr函数

devintr利用plic_claim获得设备中断的中断号，调用相应的中断处理程序uartintr

uartintr通过uartgetc获得存储在UART寄存器中的字符，调用consoleintr处理字符，写入到环形队列中，等待消费者的处理（如在接受到换行后唤醒sleep进程，由shell调用read方法取出字符）



## Lec10 Multiprocessors and locking

#### 锁的种类

自旋锁：无法获得锁，就一直循环获取，适合短时间的加锁

睡眠锁：条件锁？条件不满足则陷入睡眠并释放锁，当条件满足时，获取锁，执行下面的操作



#### 锁使用的场景

一个非常保守同时也是非常简单的规则：如果两个进程访问了一个共享的数据结构，并且其中一个进程会更新共享的数据结构，那么就需要对于这个共享的数据结构加锁。

锁的特性：

- 锁可以避免丢失更新。如果没有锁，在出现race condition的时候，内存page不会被加到freelist中。但是加上锁之后，我们就不会丢失这里的更新。

- 锁可以打包多个操作，使它们具有原子性。我们之前介绍了加锁解锁之间的区域是critical section，在critical section的所有操作会都会作为一个原子操作执行。

- 锁可以维护共享数据结构的不变性。共享数据结构如果不被任何进程修改的话是会保持不变的。如果某个进程acquire了锁并且做了一些更新操作，共享数据的不变性暂时会被破坏，但是在release锁之后，数据的不变性又恢复了。



#### 代码流程

__sync_synchronize()	加锁和critical section的代码执行通常完全相互独立，它们之间没有任何关联，因此CPU和编译器极有可能将critical section代码置于锁之外	对于synchronize指令，任何在它之前的load/store指令，都不能移动到它之后

__sync_lock_test_and_set(&lk->locked, 1)	加锁的原子操作，确保括号中的操作为原子操作，一般是使用CPU的特殊硬件指令实现	

效果：如果锁没有被持有，那么锁对象的locked字段会是0，如果locked字段等于0，我们调用test-and-set将1写入locked字段，并且返回locked字段之前的数值0。如果返回0，那么意味着没有人持有锁，循环结束。

__sync_lock_release	释放锁的原子操作，使用的原因是store指令并非一定是原子操作

加解锁的流程中需要关闭中断，防止使用锁的过程中中断，而中断处理程序又需要锁，造成死锁

#### Lab思路

COW

fork修改：  1.子进程获得父进程的页表

2.将页表内容全部置为只读

缺页中断：  1.复制出一个可写页面到进程的页表



释放空间问题：1. 初始化引用数	在哪初始化？

2. 释放时减少引用数
3. exe重置时，更新引用数
4. 引用次数的传递  地址复制还是值复制？



---

# Lec11 Thread switching

##### 线程状态

程序计数器（Program Counter），它表示当前线程执行指令的位置。

保存变量的寄存器。

程序的Stack。通常来说每个线程都有属于自己的Stack，Stack记录了函数调用的记录，并反映了当前线程的执行点。

##### xv6的线程切换

- 从一个用户进程切换到另一个用户进程，都需要从第一个用户进程接入到内核中，保存用户进程的状态并运行第一个用户进程的内核线程。

- 再从第一个用户进程的内核线程切换到第二个用户进程的内核线程。

- 之后，第二个用户进程的内核线程暂停自己，并恢复第二个用户进程的用户寄存器。

- 最后返回到第二个用户进程继续执行

#### 线程切换函数

##### swtch函数

swtch函数（避开switch关键字）会保存用户进程P1对应内核线程的寄存器至context对象。所以有两类寄存器：用户寄存器存在trapframe中，内核线程的寄存器存在context中。

实际上,swtch函数并不是直接从一个内核线程切换到另一个内核线程。XV6中，一个CPU上运行的内核线程可以直接切换到的是这个CPU对应的调度器线程。所以如果我们运行在CPU0，swtch函数会恢复之前为CPU0的调度器线程保存的寄存器和stack pointer，之后就在调度器线程的context下执行schedulder函数中。

##### schedulder函数

schedulder函数由调度器线程执行。在schedulder函数中会做一些清理工作，例如将进程P1设置成RUNABLE状态。之后再通过进程表单找到下一个RUNABLE进程。假设找到的下一个进程是P2（虽然也有可能找到的还是P1），schedulder函数会再次调用swtch函数，完成下面步骤：

1. 先保存自己的寄存器到调度器线程的context对象
2. 找到进程P2之前保存的context，恢复其中的寄存器
3. 因为进程P2在进入RUNABLE状态之前，如刚刚介绍的进程P1一样，必然也调用了swtch函数。所以之前的swtch函数会被恢复，并返回到进程P2所在的系统调用或者中断处理程序中（注，因为P2进程之前调用swtch函数必然在系统调用或者中断处理程序中）。
4. 不论是系统调用也好中断处理程序也好，在从用户空间进入到内核空间时会保存用户寄存器到trapframe对象。所以当内核程序执行完成之后，trapframe中的用户寄存器会被恢复。
5. 最后用户进程P2就恢复运行了。

##### sched函数

sched函数由用户线程调用，切换到调度器线程。与schedulder函数互为协程的关系，也将调用swtch函数。根据线程切换机制，sched调用swtch函数后，CPU的下一条指令处于schedulder函数的swtch函数后，原因是swtch函数保存了ra(返回地址)寄存器，因此sched调用swtch函数后，当前ra变成了调度器线程的ra，即上一次调度器线程调用schedulder函数时存储的ra值，故接下来执行schedulder函数swtch调用后的代码。同理，schedulder函数调用swtch函数后，CPU将转移到sched函数。



#### Lab: Multithreading

##### switching between threads

RA(返回地址)寄存器

SP(栈顶)寄存器

##### Using threads

Linux多线程编程

pthread_create	线程创建函数，在线程创建以后，就开始运行相关的线程函数。

pthread_join	等待函数，会让主线程阻塞，直到所有线程都已经退出

assert的作用是先计算表达式 expression ，如果其值为假（即为0），那么它先向stderr打印一条出错信息，然后通过调用 abort 来终止程序运行。

linux lock

```c
pthread_mutex_t lock;            // declare a lock
pthread_mutex_init(&lock, NULL); // initialize the lock
pthread_mutex_lock(&lock);       // acquire lock
pthread_mutex_unlock(&lock);     // release lock

//条件锁
pthread_cond_wait(&cond, &mutex);  // go to sleep on cond, releasing lock mutex, acquiring upon wake up
//该函数运行结束后，其还持有锁mutex，需要释放锁

pthread_cond_broadcast(&cond);     // wake up every thread sleeping on cond
```





##### lab测试

```shell
make GRADEFLAGS=sleep grade
```



# Lec13 Sleep & Wake up

##### 线程切换过程中锁的限制

进程在调用switch函数的过程中，必须要持有p->lock，但是同时又不能持有任何其他的锁

##### lost wake-up problem

由于执行顺序的原因，wake up在sleep之前被调用，导致sleep无法被唤醒。

解决方法：使用条件锁，即linux中的pthread_cond_wait

#### 代码分析

##### sleep

sleep函数，需要两把锁的使用。

首先是临界区的锁，在sleep中释放临界区锁，让生产者可以获得锁。

其次是进程锁，进程状态需要修改为sleep状态，需要加锁处理

在进入sleep状态时，获取进程锁，释放临界区锁，这里意图是解决lost wake-up问题，

指定进程的chan，修改进程状态，调用sched函数进行进程调度

在被wake up唤醒后，sleep释放进程锁，并且获得临界区锁

##### wakeup

wakeup函数循环全部进程列表，如果进程sleep在相应的chan中，则将进程状态改为可运行

在判断进程状态时，要先获取该进程锁，防止在判断语句中间，出现其他进程修改了进程状态。

##### exit

首先，关闭进程持有的文件

然后关闭对于当前目录的记录

加进程锁获取父进程

先加父进程锁，再加当前进程锁（要求整个系统的这个顺序一致）

唤醒父进程，修改当前进程的状态为ZOMBIE，将子进程的父进程重设为initproc

最后，调用sched函数进行进程调度

注：在结束进程时，进程无法自己释放自身的页表和堆栈，因此使用ZOMBIE状态，父进程在检测到子进程的ZOMBIE状态后，会将其资源释放，而后结束进程

在Unix中，对于每一个退出的进程，都需要有一个对应的wait系统调用，因此需要将结束进程的子进程的父进程设置为initproc进程

##### wait

Unix中wait调用会等待一个子进程结束，并返回其pid（xv6一样）

wait函数包含一个无限循环，循环内部遍历进程表，找到子进程，如果子进程为ZOMBIE，父进程将释放其资源，然后将进程状态设置为unused，并将pid返回

如果子进程都没结束，则当前进程陷入sleep，chan为自己本身，lock为当前进程锁

##### kill

kill操作一般会带来较大的风险，因此，在XV6和其他的Unix系统中，kill系统调用基本上不做任何事情。

故实际中，kill函数主要是循环进程表，找到待kill进程，将其killed标志设置为1，如果待kill进程处于sleep状态，需要将其唤醒

killed标志被设置后，进程会在一些安全的位置判断，并退出，xv6中主要是中断处理程序中以及pipe中。




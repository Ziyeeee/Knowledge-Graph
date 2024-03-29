# 任务：关联规则挖掘

<通常的做法是挖掘隐藏在数据中的相互关系，当两个或多个数据项的取值相互间高概率的重复出现时，那么就会认为它们之间存在一定的关联。>


## 概念：关联

<关联就是反映某个事物与其他事物之间相互依存关系>


### 属性：关联就是反映某个事物与其他事物之间相互依存关系

## 概念：关联分析

<关联分析是指在交易数据中，找出存在于项目集合之间的关联模式，即如果两个或多个事物之间存在一定的关联性，则其中一个事物就能通过其他事物进行预测。>


### 属性：关联分析是指在数据中，找出存在于项目集合之间的关联模式

### 属性：如果两个或多个事物之间存在一定的关联性，则其中一个事物就能通过其他事物进行预测

## 概念：事务

<数据通常以二维表的形式展示，如表18-1所示，每一行都对应一个事务。>


### 属性：数据通常以二维表的形式展示，每一行都对应一个事务

### 概念：项

<对于每行事务，其中包含的每个商品都称为项。>


- 属性：对于每行事务，其中包含的每个商品都称为项
- 概念：项集

  <在关联分析中，包含零个或多个项的集合称为项集。>
  

	- 属性：在关联分析中，包含零个或多个项的集合称为项集
	- 概念：k-项集

	  <如果一个项集包含k个项，则称它为k-项集。 例如，{I1，I2，I4}是一个三项集。>
	  

		- 属性：如果一个项集包含k个项，则称它为k-项集

	- 概念：空集

	  <空集则是不包含任何项的项集。>
	  

		- 属性：不包含任何项的项集

	- 概念：支持度计数

	  <项集有一个重要的属性，称为支持度计数，是指在数据库中包含该项集的事务个数，也称为出现频度。>
	  

		- 属性：在数据库中包含该项集的事务个数
		- 属性：具体定义为:σ(X)=|{t_i|X⊑t_i,t_i∈T}|

			- 概念：|•|

			  <其中，符号|•|表示集合中元素的个数。>
			  

				- 属性：表示集合中元素的个数

## 概念：关联规则

<关联规则是形如的蕴涵表达式，其中X和Y是不相交的两个项集。>


### 属性：形如X→Y的蕴涵表达式，其中X和Y是不相交的两个项集

## 概念：支持度

<其中support是支持度，可以用于给定数据集的频繁程度，表示所有事务的40%显示机械键盘和笔记本保护套被同时购买；>


### 属性：用于给定数据集的频繁程度

### 属性：s(X→Y)=(σ(X∪Y))/N

### 概念：最小支持度阈值

<为了筛选出有用的关联规则，我们需要根据应用场景设定相应的阈值，分别是最小支持度阈值（minsup）和最小置信度阈值（minconf）。>


## 概念：置信度

<confidence是置信度，可以用于确定后者在包含前者的事务中出现的频繁程度，表示购买笔记本保护套的顾客中80%也购买了机械键盘。>


### 属性：用于确定后者在包含前者的事务中出现的频繁程度

### 属性：c(X→Y)=(σ(X∪Y))/(σ(X))

### 概念：最小置信度阈值

<为了筛选出有用的关联规则，我们需要根据应用场景设定相应的阈值，分别是最小支持度阈值（minsup）和最小置信度阈值（minconf）。>


## 概念：频繁项集

<如果它的支持度满足最小支持度阈值，则称它为频繁项集，频繁k项集的集合通常记为L_k。>


### 属性：对于项集来说，如果它的支持度满足最小支持度阈值，则称它为频繁项集

### 属性：频繁k项集的集合通常记为L_k

## 概念：强规则

<对于规则来说，如果它同时满足最小支持度阈值和最小置信度阈值，则称它为强规则。>


### 属性：对于关联规则来说，如果它同时满足最小支持度阈值和最小置信度阈值，则称它为强规则

## 属性：当两个或多个数据项的取值相互间高概率的重复出现时，那么就会认为它们之间存在一定的关联

## 属性：分类

<由于在不同的应用场景下，数据形式也会有所不同，挖掘得到的关联规则也会不同。我们基于不同的考量，给出三种常用的关联规则分类>


### 属性：基于规则所涉及的维数

- 任务：单维关联规则

  <单维关联规则： 若关联规则中的项或属性只涉及一个维，则称它为单维关联规则。单维关联规则展示了同一个属性或维内的联系。>
  

	- 属性：若关联规则中的项或属性只涉及一个维，则称它为单维关联规则

		- 概念：维

		   <按照多维数据库使用的术语，通常将规则中的不同谓词称作维。>
		  

			- 属性：按照多维数据库使用的术语，通常将规则中的不同谓词称作维

- 任务：多维关联规则

  <多维关联规则： 若关联规则中的项或属性涉及两个及以上的维，则称它为多维关联规则。多维关联规则展示了不同属性或维之间的关联。>
  

	- 属性：若关联规则中的项或属性涉及两个及以上的维，则称它为多维关联规则

### 属性：基于规则所处理的类型

- 任务：布尔关联规则

  <布尔关联规则： 若关联规则只考虑项是否出现，而不涉及具体的取值，则它是布尔关联规则。例如，在关联规则18-3中，它只考虑顾客是否购买laptop和keyboard，而不考虑顾客购买的laptop的价格等属性，所以它是布尔关联规则。>
  

	- 属性：若关联规则只考虑项是否出现，而不涉及具体的取值，则它是布尔关联规则

- 任务：量化关联规则

  <量化关联规则： 若关联规则中还考虑了量化的项或属性之间的关联，则它是量化关联规则。在量化关联规则中，部分项或属性的值被划分为区间，这些属性被称为量化属性。例如在关联规则18-4中，age和income都是量化属性，所以该规则是量化关联规则。注意，量化关联规则中也能包含非量化的项或属性，例如规则18-4中的buys。>
  

	- 属性：若关联规则中还考虑了量化的项或属性之间的关联，则它是量化关联规则

### 属性：基于所挖掘的数据类型和特性

- 任务：时序模式关联规则

  <时序模式关联规则： 在一些应用场景中，关联规则可能涉及到序列特征，即存在基于时间或空间的先后次序。例如：通过店铺订单数据，我们可能发现顾客会先购买PC，再购买机械键盘、显示器等外设，接着购买电脑保护套、键盘清洁泥等小工具。这就是一种序列模式。时序模式关联规则就是包含序列模式信息的关联规则。>
  

	- 属性：时序模式关联规则就是包含序列模式信息的关联规则

		- 概念：序列特征

			- 属性：关联规则中存在基于时间或空间的先后次序

- 任务：结构模式关联规则

  <结构模式关联规则： 结构模式是指结构数据集中的频繁子结构。与序列相比，结构是一个更一般的概念，包括有向图、无向图、格、树、序列、集合等，单个项可以看作是最简单的结构模式。结构模式关联规则就是挖掘结构模式得到的关联规则。>
  

	- 属性：结构模式关联规则就是挖掘结构模式得到的关联规则

		- 概念：结构模式

			- 属性：结构模式是指结构数据集中的频繁子结构

## 属性：基本框架

<关联规则挖掘任务通常分为两个子任务。（1）频繁项集发现：目标是找出所有满足最小支持度阈值的项集，这些项集被称为频繁项集。（2）关联规则产生：目标是从发现的频繁项集中提取出所有满足最小置信度阈值的规则，这些规则被称为强规则。>


### 任务：1.频繁项集发现

<频繁项集发现：目标是找出所有满足最小支持度阈值的项集，这些项集被称为频繁项集。>


- 方法：朴素的频繁项集挖掘

  <从频繁项集的定义出发，我们只需要计算出每个项集的支持度，再将其与最小支持度阈值比较，满足的即为频繁项集。要计算候选项集的支持度，我们需要确定候选项集的支持度计数。而确定支持度计数的方法很简单，只需要将候选项集与每个事务进行比较，如果候选项集包含在事务中，就增加它的支持度计数。>  
  

	- 任务：1.计算出每个项集的支持度

		- 任务：1.确定候选项集的支持度计数

			- 任务：1.将候选项集与每个事务进行比较
			- 任务：2.如果候选项集包含在事务中，就增加它的支持度计数

	- 任务：2.与最小支持度阈值比较
	- 任务：3.满足的即为频繁项集
	- 属性：缺点

		- 属性：计算开销大

			- 属性：需要进行O(NMw)次比较

				- 属性：N是事务数
				- 属性：M=2^k-1是候选项集数（不含空集）
				- 属性：w是事务的最大宽度

### 任务：2.关联规则产生

<关联规则产生：目标是从发现的频繁项集中提取出所有满足最小置信度阈值的规则，这些规则被称为强规则。得到频繁项集后，我们需要从这些频繁项集中提取出关联规则（强规则）。提取的方式可以简要地概括如下：将频繁项集Y划分成两个非空子集和，得到候选关联规则，然后计算该候选关联规则的置信度，若满足最小置信度阈值，则该关联规则就是强规则，否则舍弃。注意，和必须是非空子集，因为和没有实际意义。>


- 任务：1.将频繁项集Y划分成两个非空子集X和Y-X

	- 属性：X和Y-X必须是非空子集，因为∅→Y和Y→∅没有实际意义

- 任务：2.得到候选关联规则X→Y-X
- 任务：3.计算该候选关联规则的置信度
- 任务：4.满足最小置信度阈值，则该关联规则就是强规则，否则舍弃
- 属性：每个频繁k-项集能够产生2^k-2个候选关联规则

*XMind - Trial Version*
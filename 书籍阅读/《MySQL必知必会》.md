# 《MySQL必知必会》

1. 浮点型数据不精准，定点数类型--DECIMAL数据精准

2. **修改字段**数据类型
   
   1. `alter table xxx modify column ziduan DECIMAL(5,2)`
   
3. 创建表

   ~~~mysql
   CREATE table demo.importhead(
   	 listnumber INT,
   	supplierid INT,
   	stocknumber INT,
       --我们在字段importype定义为INT类型的后面，按照MySQL创建表的语法，加了默认值1。
   	importtype int default 1,
   	quantity decimal(10,3),
   	importvalue decimal(10,2),
   	recorder int,
   	recordingdate datetime
   
   );
   ~~~

4. 插入一条记录

   ~~~mysql
   -- 插入一条记录 INSERT INTO 表名 [(字段名 [,字段名] ...)] VALUES (值的列表);
   INSERT INTO demo.importhead
   (
   	listnumber,
   	supplierid,
   	stocknumber,
   	-- 这里我们没有插入字段importtype的值
   	quantity,
   	importvalue,
   	recorder,
   	recordingdate
   ) VALUES(
   	3456,
   	1,
   	1,
   	10,
   	100,
   	1,
   	'2020-12-10'
   	
   );
   ~~~

5.  约束

   + 默认约束：设置了默认约束，插入数据的时候，如果不明确给字段赋值，那么系统会把设置的默认值自动赋值给字段。

6. 克隆表

   ~~~mysql
   create table demo.importheadhist like demo.importhead;
   ~~~

7. 增加字段

   ~~~mysql
   alter table demo.importheadhist add confirmer text;
   alter table demo.importheadhist add confirmdate datetime;
   
   ~~~

8. 修改字段

   ~~~mysql
   alter table demo.importheadhist CHANGE quantity importquantity DOUBLE;
   ~~~

9. 插入查询结果

   ~~~mysql
   INSERT INTO 表名 （字段名）
   SELECT 字段名或值
   FROM 表名
   WHERE 条件
   
   
   ~~~

10. 删除数据

    ~~~mysql
    DELETE FROM 表名 
    WHERE 条件
    ~~~

11. 修改数据

    ~~~mysql
    UPDATE 表名
    SET 字段名=值
    WHERE 条件
    ~~~

12. 查询数据

    ~~~mysql
    SELECT *|字段列表
    FROM 数据源
    WHERE 条件
    GROUP BY 字段
    HAVING 条件
    ORDER BY 字段
    LIMIT 起始点，行数
    ~~~

13. 创建数据库

    ~~~mysql
    
    ~~~

    



LOAD_MEM 0       ; Загрузка первого элемента вектора
LOAD_CONST 193   ; Загрузка константы 193
OR 0             ; Побитовое "или" и запись обратно
STORE            ; Сохранение результата в память по адресу из стека

LOAD_MEM 1       ; Загрузка второго элемента вектора
LOAD_CONST 193
OR 1
STORE

LOAD_MEM 2
LOAD_CONST 193
OR 2
STORE

LOAD_MEM 3
LOAD_CONST 193
OR 3
STORE

LOAD_MEM 4
LOAD_CONST 193
OR 4
STORE

# chatbot_sql

**chatbot_sql** is a terminal-based Python application that translates natural language questions in **Portuguese** into executable **SQLite** queries using a local **LLM (Mistral-7B)** running on CPU. It also includes a utility to populate the database from an Excel (.xlsx) file.

---

## Features

- Converts questions in **Portuguese** to SQL queries using an LLM.
- Extracts database schema automatically and includes it in the prompt.
- Built-in SQL safety checks to block dangerous commands (`DROP`, `DELETE`, etc.).
- Populates an SQLite database from a raw Excel file with realistic fake client data.
- Uses `llama-cpp-python` to run Mistral-7B locally (no GPU required).

---

## Project Structure

```bash
.
├── text2sql_script.py     # Run chatbot to ask questions
├── database/
│   └── vendas_retail.db   # Generated SQLite database
│   └── populate_db.py     # Populate the SQLite DB from Excel
│   └── raw_data.xlsx          # Input Excel file with raw sales data
├── requirements.txt       # Python requirements for the project
├── models/                # LLM model file
│   └──# Put the models files here
└── README.md

```


## Instructions
1. Create and activate a Python env
```bash
    python3 -m venv .venv
    source .venv/bin/activate
```
2. Install the dependencies
```bash
  pip install -r requirements.txt
```
3. Download the LLM you would like to use on the 'models/' folder
```bash
wget  "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
```
4. Run the populate database script to generate the db file:
```bash
python database/populate_db.py
```
5. Run the script for the tool
```bash
python text2sql_script.py
```
6. Write the query you want in Portuguese


## Tests
1. Sua pergunta: Qual o faturamento total por produto?
-------Query gerada-------
 ```sql
SELECT products.name, SUM(products.unit_price * sales.quantity) AS total_revenue
FROM products
JOIN sales ON products.product_id = sales.product_id
GROUP BY products.name;
```
Resultado:
                                  name  total_revenue
0                 Air Fryer Mondial 4L         533630
1               Aspirador de Pó Philco         483420
2                  Bicicleta Caloi 100        1759800
3           Bola de Futebol Nike Campo         271400
4                 Boné New Era Yankees         235440
5     Cafeteira Nespresso Essenza Mini         619320
6                Caixa de Som JBL Go 3         271170
7               Calça Legging Nike Pro         381080
8   Carregador Portátil Anker 10000mAh         222660
9                Console PlayStation 5        2227005
10              Câmera Canon EOS Rebel        2185600
11                    Drone DJI Mini 2        1913953
12           Esteira Elétrica Movement        1886850
13                Fogão Consul 4 bocas        1258100
14       Fone Bluetooth Samsung Buds 2         769599
15                  Fone de Ouvido JBL         395150
16             Geladeira Brastemp 375L        2252250
17       Headset Gamer HyperX Cloud II         598520
18      Impressora Epson EcoTank L3250        1355165
19               Impressora HP DeskJet         593760
20          Jaqueta Corta Vento Adidas         522900
21              Micro-ondas Electrolux         786160
22        Mochila Lenovo para notebook         184200
23                      Monitor LG 24"        1165200
24     Mouse Gamer Razer DeathAdder V2         368960
25                 Mouse Logitech M170          92025
26               Máquina de Lavar 11kg        1660600
27              Notebook Dell Inspiron        2515500
28       Patins Rollerblade Zetrablade        1023961
29      Placa de Vídeo Nvidia RTX 4060        2291045
30           Relógio Smartwatch Xiaomi         518400
31                SSD Kingston NV2 1TB         600480
32                Smart TV Samsung 50"        1992300
33         Smartphone Motorola Edge 40        2425726
34              Smartphone Samsung A34        1732437
35                Smartphone iPhone 14         224970
36            Soundbar Samsung HW-T450        1294704
37     Teclado Logitech K380 Bluetooth         280500
38           Teclado Mecânico Redragon         297750
39               Tênis Nike Revolution         407040
40             Ventilador Mondial 40cm         246800
41      Óculos de Sol Ray-Ban Wayfarer         761360


2. Qual o total de vendas por produto?
-------Query gerada-------
 ```sql
SELECT products.name, SUM(sales.quantity) AS total_sales
FROM clients
JOIN sales ON clients.client_id = sales.client_id
JOIN products ON sales.product_id = products.product_id
GROUP BY products.name;
```
Resultado:
                                  name  total_sales
0                 Air Fryer Mondial 4L         1241
1               Aspirador de Pó Philco         1151
2                  Bicicleta Caloi 100          838
3           Bola de Futebol Nike Campo         1180
4                 Boné New Era Yankees         1308
5     Cafeteira Nespresso Essenza Mini         1191
6                Caixa de Som JBL Go 3         1179
7               Calça Legging Nike Pro         1361
8   Carregador Portátil Anker 10000mAh         1237
9                Console PlayStation 5          495
10              Câmera Canon EOS Rebel          683
11                    Drone DJI Mini 2          547
12           Esteira Elétrica Movement          315
13                Fogão Consul 4 bocas         1094
14       Fone Bluetooth Samsung Buds 2         1101
15                  Fone de Ouvido JBL         1129
16             Geladeira Brastemp 375L          585
17       Headset Gamer HyperX Cloud II         1151
18      Impressora Epson EcoTank L3250         1085
19               Impressora HP DeskJet         1237
20          Jaqueta Corta Vento Adidas         1162
21              Micro-ondas Electrolux         1268
22        Mochila Lenovo para notebook         1228
23                      Monitor LG 24"          971
24     Mouse Gamer Razer DeathAdder V2         1153
25                 Mouse Logitech M170         1227
26               Máquina de Lavar 11kg          722
27              Notebook Dell Inspiron          559
28       Patins Rollerblade Zetrablade         1139
29      Placa de Vídeo Nvidia RTX 4060          955
30           Relógio Smartwatch Xiaomi         1080
31                SSD Kingston NV2 1TB         1251
32                Smart TV Samsung 50"          687
33         Smartphone Motorola Edge 40          674
34              Smartphone Samsung A34          963
35                Smartphone iPhone 14           30
36            Soundbar Samsung HW-T450         1296
37     Teclado Logitech K380 Bluetooth         1122
38           Teclado Mecânico Redragon         1191
39               Tênis Nike Revolution         1272
40             Ventilador Mondial 40cm         1234
41      Óculos de Sol Ray-Ban Wayfarer         1228


3. Sua pergunta: Qual o faturamento total por loja?
-------Query gerada-------
 ```sql
SELECT stores.region, stores.address, SUM(sales.quantity * products.unit_price) AS total_revenue
FROM sales
JOIN clients ON sales.client_id = clients.client_id
JOIN products ON sales.product_id = products.product_id
JOIN stores ON sales.store_id = stores.store
GROUP BY stores.region, stores.address;
```
Resultado:
          region                                            address  total_revenue
0   Centro-Oeste  Estação Almeida, 45, Vila Independencia 3ª Seç...        1227703
1   Centro-Oeste  Recanto Azevedo, 79, Ventosa, 77622021 Araújo ...        1306735
2   Centro-Oeste  Rodovia de Monteiro, Novo Tupi, 03412750 Viana...         969259
3       Nordeste  Chácara Vargas, 55, Santa Terezinha, 90769890 ...        4201956
4       Nordeste  Ladeira Moraes, 47, Luxemburgo, 57679-546 Mont...        3517340
5       Nordeste  Vale Mariane Vargas, 1, Universitário, 71041-2...        3251178
6          Norte  Esplanada de Peixoto, 82, Boa Vista, 28204750 ...        1217352
7          Norte  Loteamento Silva, 89, Vila Barragem Santa Lúci...        1159089
8          Norte  Via Olívia Fernandes, Vila Das Oliveiras, 3338...         831412
9        Sudeste  Feira de Jesus, Cinquentenário, 96460847 Rocha...        6234515
10       Sudeste  Lago João Costela, 95, Pompéia, 24286-130 Nova...        5715486
11       Sudeste  Praça Barbosa, 7, Delta, 15298061 da Cunha de ...        5893527
12           Sul  Estação de Campos, 53, Vila Piratininga, 24326...        2088703
13           Sul  Lagoa Borges, 29, Vila Santa Rosa, 34686297 Na...        1871971
14           Sul  Trevo de Ferreira, 68, Santana Do Cafezal, 261...        2120664

4. Sua pergunta: Quais os vendedores com os maiores números de pedidos?
-------Query gerada-------
 ```sql
SELECT sellers.name, COUNT(*) as order_count
FROM sales
INNER JOIN sellers ON sales.seller_id = sellers.seller_id
INNER JOIN clients ON sales.client_id = clients.client_id
GROUP BY sellers.name
ORDER BY order_count DESC;
```
Resultado:
      name  order_count
0  Cecília          910
1    Alice          895
2  Antônio          884
3   Samuel          869
4   Helena          866
5    Artur          852
6   Miguel          841
7     Davi          823
8    Laura          819
9    Maitê          814

5. Sua pergunta: Qual o número de vendas por forma de pagamento?
-------Query gerada-------
 ```sql
SELECT 
    payment,
    COUNT(*) AS sales_count
FROM 
    sales
GROUP BY 
    payment;
```
Resultado:
   payment  sales_count
0     None         1747
1   Boleto         1685
2  Crédito         1777
3   Débito         1711
4      Pix         1653

6. Qual o faturamento por categoria de produto?
-------Query gerada-------
 ```sql
SELECT products.category, SUM(sales.quantity * products.unit_price) AS total_billing
FROM sales
JOIN products ON sales.product_id = products.product_id
GROUP BY products.category;
```
Resultado:
            category  total_billing
0         Acessórios        1686620
1   Eletrodomésticos        5957110
2    Eletroportáteis        1883170
3        Eletrônicos        8318858
4           Esportes        4942011
5        Impressoras        1948925
6        Informática        6572225
7        Periféricos        1039235
8          Telefonia        5152732
9          Vestuário        1546460
10             Áudio        2559544









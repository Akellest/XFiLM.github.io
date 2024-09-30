<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Tables</title>
    <link rel="stylesheet" href="styles.css"> <!-- Общий стиль для таблиц -->
    <style>
        /* Общий стиль для всех таблиц */
        .table {
            border-collapse: collapse;
            width: 100%; /* Занять всю ширину контейнера */
            margin-bottom: 20px;
        }

        .table td, .table th {
            border: 2px solid;
            padding: 10px;
            text-align: center;
            vertical-align: middle;
        }

        /* Стили для каждой таблицы */
        .table1 td {
            border-color: #CC0000; /* Цвет границы для первой таблицы */
        }
        .table2 td {
            border-color: #CEE2F3; /* Цвет границы для второй таблицы */
        }
        .table3 td {
            border-color: #4986E8; /* Цвет границы для третьей таблицы */
        }
    </style>
</head>
<body>

    <h1>Combined Tables</h1>

    <div class="table1">
        <h2>Table 1</h2>
        <table class="table"> <!-- Применяем общий стиль -->
            <?php include 'table1.html'; ?>
        </table>
    </div>

    <div class="table2">
        <h2>Table 2</h2>
        <table class="table"> <!-- Применяем общий стиль -->
            <?php include 'table2.html'; ?>
        </table>
    </div>

    <div class="table3">
        <h2>Table 3</h2>
        <table class="table"> <!-- Применяем общий стиль -->
            <?php include 'table3.html'; ?>
        </table>
    </div>

</body>
</html>
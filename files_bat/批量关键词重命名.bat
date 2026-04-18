@echo off
setlocal enabledelayedexpansion

:: --------------------------
:: 1. 输入并验证目标目录
:: --------------------------
:input_dir
set /p "target_dir=请输入要操作的目录路径（例如 D:\Documents）: "
if not exist "%target_dir%\" (
    echo 错误：目录 "%target_dir%" 不存在，请重新输入！
    goto input_dir
)

:: --------------------------
:: 2. 输入并验证「查找关键词」
:: --------------------------
:input_find
set /p "find_key=请输入要查找的文件名关键字: "
if "%find_key%"=="" (
    echo 错误：查找关键字不能为空，请重新输入！
    goto input_find
)

:: --------------------------
:: 3. 输入并验证「替换关键词」
:: --------------------------
:input_replace
set /p "rep_key=请输入要替换的新关键字: "
if "%rep_key%"=="" (
    echo 错误：替换关键字不能为空，请重新输入！
    goto input_replace
)

:: --------------------------
:: 4. 遍历文件 + 批量重命名（修复版）
:: --------------------------
echo.
echo 正在处理目录 "%target_dir%" 下的文件（将 "%find_key%" 替换为 "%rep_key%"）...
set total_found=0       :: 找到的匹配文件总数
set success_rename=0    :: 成功重命名的数量

:: 切换到目标目录处理
pushd "%target_dir%"

for %%f in (*%find_key%*) do (
    :: 排除子文件夹（仅处理文件）
    if not exist "%%f\" (
        set /a total_found+=1
        set "old_name=%%f"          :: 原文件名（含扩展名）
        set "new_name=!old_name:%find_key%=%rep_key%!"  :: 替换后的新文件名
        
        :: 跳过「替换后文件名无变化」的情况
        if not "!old_name!"=="!new_name!" (
            echo 正在重命名："!old_name!" → "!new_name!"
            ren "!old_name!" "!new_name!"
            
            :: 检查是否成功
            if !errorlevel!==0 (
                set /a success_rename+=1
                echo  → 成功！
            ) else (
                echo  → 失败！
            )
        ) 
    )
)

:: 返回原始目录
popd

:: --------------------------
:: 5. 输出最终统计
:: --------------------------
echo.
echo 处理完成！
echo   - 找到含 "%find_key%" 的文件总数：%total_found%
echo   - 成功重命名的文件数：%success_rename%

pause
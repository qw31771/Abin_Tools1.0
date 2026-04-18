@echo off
setlocal enabledelayedexpansion

echo =============================================
echo Maya 文件整理脚本（自动处理 .ma 和 .mb 文件）
echo =============================================
echo.

:: 模式选择（0=默认整理 / 1=整理+复制特殊文件）
:select_mode
set /p mode="请选择操作模式（输入0为默认整理，1为添加复制文件功能）："
if "%mode%" neq "0" if "%mode%" neq "1" (
    echo 输入错误！请输入0或1
    goto select_mode
)

:: 提示用户输入目标目录
set /p target_dir="请输入要处理的目录路径（例如 D:\Maya_Projects）："

:: 检查路径是否存在
if not exist "%target_dir%\" (
    echo 错误：指定的路径不存在！
    pause
    exit /b
)

echo.
echo 正在处理目录：%target_dir%
echo.

:: 获取批处理文件所在目录（用于定位"不能删.ma"）
set "bat_dir=%~dp0"
set "special_ma=%bat_dir%不能删.ma"

:: 进入目标目录（避免影响当前目录）
pushd "%target_dir%" || (
    echo 错误：无法进入目录！
    pause
    exit /b
)

:: 处理 .ma 和 .mb 文件
for %%f in (*.ma *.mb) do (
    if not "%%f"=="%~nx0" (  :: 排除批处理自身
        set "file_name=%%~nf"
        set "file_ext=%%~xf"
        
        :: 创建基础文件夹（如果不存在）
        if not exist "!file_name!" (
            md "!file_name!"
            md "!file_name!\Model"
            md "!file_name!\Rig"
            
            :: 默认操作：移动Maya文件到Model
            move "%%f" "!file_name!\Model"
            echo 已移动：%%f → !file_name!\Model
            
            :: 扩展操作（模式1）：复制特殊文件到Rig
            if "%mode%"=="1" (
                if exist "!special_ma!" (
                    set "target_path=!file_name!\Rig\%%~nf.ma"
                    copy /y "!special_ma!" "!target_path!" >nul
                    echo 已复制特殊文件到：!target_path!
                ) else (
                    echo 警告：未找到特殊文件"不能删.ma"（批处理目录：%bat_dir%）
                )
            )
        ) else (
            echo 跳过已存在文件夹：%%f（目标路径：%%~nf）
        )
    )
)

:: 返回原目录
popd

echo.
echo 操作完成！
echo 按任意键关闭...
pause >nul
endlocal
exit

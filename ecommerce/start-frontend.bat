@echo off
echo 🚀 Starting ShopFlow E-Commerce Frontend...
echo.

cd frontend

echo 📦 Installing dependencies...
call npm install

echo.
echo 🎨 Starting development server...
echo Frontend will be available at: http://localhost:3000
echo API Backend is at: http://localhost:8000
echo.

call npm start

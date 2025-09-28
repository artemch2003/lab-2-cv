"""
Упрощенная рабочая версия современного интерфейса без сложных стилей.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
from PIL import Image, ImageTk

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SimpleModernPhotoEditor:
    """Упрощенный современный фоторедактор."""
    
    def __init__(self, root):
        """Инициализация редактора."""
        self.root = root
        self.original_image = None
        self.processed_image = None
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        """Настройка главного окна."""
        self.root.title("Photo Editor Pro - Обработка изображений")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
    def create_interface(self):
        """Создание интерфейса."""
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        self.create_header(main_frame)
        
        # Основная рабочая область
        self.create_workspace(main_frame)
        
        # Нижняя панель
        self.create_bottom_panel(main_frame)
    
    def create_header(self, parent):
        """Создает заголовок приложения."""
        header_frame = tk.Frame(parent, bg="#2b2b2b")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Логотип и название
        title_label = tk.Label(header_frame, text="Photo Editor Pro", 
                              font=("Segoe UI", 18, "bold"), 
                              fg="#ffffff", bg="#2b2b2b")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Панель управления
        control_frame = tk.Frame(header_frame, bg="#2b2b2b")
        control_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Кнопки управления
        load_btn = tk.Button(control_frame, text="📁 Загрузить", 
                            font=("Segoe UI", 10, "bold"),
                            bg="#0078d4", fg="#ffffff", 
                            relief="flat", padx=15, pady=5,
                            command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(control_frame, text="💾 Сохранить", 
                            font=("Segoe UI", 10, "bold"),
                            bg="#0078d4", fg="#ffffff", 
                            relief="flat", padx=15, pady=5,
                            command=self.save_image)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(control_frame, text="🔄 Сброс", 
                             font=("Segoe UI", 10, "bold"),
                             bg="#0078d4", fg="#ffffff", 
                             relief="flat", padx=15, pady=5,
                             command=self.reset_image)
        reset_btn.pack(side=tk.LEFT, padx=5)
    
    def create_workspace(self, parent):
        """Создает основную рабочую область."""
        workspace_frame = tk.Frame(parent, bg="#2b2b2b")
        workspace_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        workspace_frame.columnconfigure(0, weight=2)
        workspace_frame.columnconfigure(1, weight=1)
        
        # Область отображения изображений
        self.create_image_area(workspace_frame)
        
        # Панель настроек
        self.create_settings_panel(workspace_frame)
    
    def create_image_area(self, parent):
        """Создает область отображения изображений."""
        # Контейнер для изображений
        display_frame = tk.Frame(parent, bg="#3c3c3c", relief="solid", bd=1)
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = tk.Label(display_frame, text="Изображения", 
                              font=("Segoe UI", 12, "bold"), 
                              fg="#ffffff", bg="#3c3c3c")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Исходное изображение
        original_frame = tk.Frame(display_frame, bg="#3c3c3c")
        original_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 5), pady=(0, 10))
        
        original_title = tk.Label(original_frame, text="Исходное изображение", 
                                 font=("Segoe UI", 10, "bold"), 
                                 fg="#ffffff", bg="#3c3c3c")
        original_title.pack(pady=(10, 5))
        
        self.original_canvas = tk.Canvas(original_frame, bg="#1e1e1e", height=300, highlightthickness=0)
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.original_canvas.create_text(200, 150, text="Загрузите изображение\nдля начала работы", 
                                        fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
        
        # Обработанное изображение
        processed_frame = tk.Frame(display_frame, bg="#3c3c3c")
        processed_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 10), pady=(0, 10))
        
        processed_title = tk.Label(processed_frame, text="Обработанное изображение", 
                                  font=("Segoe UI", 10, "bold"), 
                                  fg="#ffffff", bg="#3c3c3c")
        processed_title.pack(pady=(10, 5))
        
        self.processed_canvas = tk.Canvas(processed_frame, bg="#1e1e1e", height=300, highlightthickness=0)
        self.processed_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.processed_canvas.create_text(200, 150, text="Примените преобразование\nдля просмотра результата", 
                                         fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
    
    def create_settings_panel(self, parent):
        """Создает панель настроек."""
        settings_frame = tk.Frame(parent, bg="#3c3c3c", relief="solid", bd=1)
        settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Заголовок
        title_label = tk.Label(settings_frame, text="Настройки преобразования", 
                              font=("Segoe UI", 12, "bold"), 
                              fg="#ffffff", bg="#3c3c3c")
        title_label.pack(pady=15)
        
        # Тип преобразования
        type_label = tk.Label(settings_frame, text="Тип преобразования:", 
                             font=("Segoe UI", 10), 
                             fg="#ffffff", bg="#3c3c3c")
        type_label.pack(anchor=tk.W, padx=15, pady=(0, 5))
        
        self.transform_var = tk.StringVar(value="Логарифмическое")
        transform_combo = ttk.Combobox(settings_frame, 
                                     textvariable=self.transform_var,
                                     values=["Логарифмическое", "Степенное", "Бинарное", "Вырезание диапазона яркостей"], 
                                     state="readonly", width=20)
        transform_combo.pack(fill=tk.X, padx=15, pady=(0, 10))
        transform_combo.bind("<<ComboboxSelected>>", self.on_transform_change)
        
        # Описание
        desc_label = tk.Label(settings_frame, text="Описание:", 
                               font=("Segoe UI", 10), 
                               fg="#ffffff", bg="#3c3c3c")
        desc_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.desc_text = tk.Text(settings_frame, height=4, width=25, wrap=tk.WORD, 
                               bg="#2b2b2b", fg="#ffffff", font=('Segoe UI', 9),
                               relief="solid", bd=1)
        self.desc_text.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.desc_text.insert(1.0, "Логарифмическое преобразование улучшает видимость деталей в темных областях изображения.")
        self.desc_text.configure(state=tk.DISABLED)
        
        # Кнопка применения
        apply_btn = tk.Button(settings_frame, text="✨ Применить преобразование", 
                            font=("Segoe UI", 10, "bold"),
                            bg="#28a745", fg="#ffffff", 
                            relief="flat", padx=10, pady=8,
                            command=self.apply_transform)
        apply_btn.pack(fill=tk.X, padx=15, pady=10)
        
        # Обновляем описание
        self.on_transform_change()
    
    def create_bottom_panel(self, parent):
        """Создает нижнюю панель."""
        # Информационная панель
        info_frame = tk.Frame(parent, bg="#3c3c3c", relief="solid", bd=1)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        info_title = tk.Label(info_frame, text="Информация", 
                             font=("Segoe UI", 12, "bold"), 
                             fg="#ffffff", bg="#3c3c3c")
        info_title.pack(pady=(10, 5))
        
        self.info_text = tk.Text(info_frame, height=3, wrap=tk.WORD, 
                               bg="#2b2b2b", fg="#ffffff", font=('Segoe UI', 9),
                               relief="solid", bd=1)
        self.info_text.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.info_text.insert(1.0, "Информация об изображении:\nИзображение не загружено")
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = tk.Label(parent, textvariable=self.status_var, 
                             font=("Segoe UI", 8), 
                             fg="#ffffff", bg="#3c3c3c",
                             relief="flat")
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def load_image(self):
        """Загружает изображение."""
        file_types = [
            ("Изображения", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
            ("PNG файлы", "*.png"),
            ("JPEG файлы", "*.jpg *.jpeg"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_original_image()
                self.update_info(f"Изображение загружено: {os.path.basename(file_path)}")
                self.status_var.set(f"Изображение загружено: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")
                self.status_var.set("Ошибка загрузки изображения")
    
    def display_original_image(self):
        """Отображает исходное изображение."""
        if self.original_image:
            # Изменяем размер для отображения
            display_size = (400, 300)
            display_image = self.original_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Очищаем canvas и отображаем изображение
            self.original_canvas.delete("all")
            self.original_canvas.create_image(200, 150, image=photo)
            self.original_canvas.image = photo  # Сохраняем ссылку
    
    def apply_transform(self):
        """Применяет преобразование."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        transform_type = self.transform_var.get()
        self.status_var.set(f"Применение {transform_type.lower()} преобразования...")
        
        try:
            # Здесь должна быть логика применения преобразований
            # Для демонстрации просто копируем изображение
            self.processed_image = self.original_image.copy()
            self.display_processed_image()
            self.update_info(f"Применено преобразование: {transform_type}")
            self.status_var.set(f"{transform_type} преобразование применено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось применить преобразование: {e}")
            self.status_var.set("Ошибка применения преобразования")
    
    def display_processed_image(self):
        """Отображает обработанное изображение."""
        if self.processed_image:
            # Изменяем размер для отображения
            display_size = (400, 300)
            display_image = self.processed_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Очищаем canvas и отображаем изображение
            self.processed_canvas.delete("all")
            self.processed_canvas.create_image(200, 150, image=photo)
            self.processed_canvas.image = photo  # Сохраняем ссылку
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        if not self.processed_image:
            messagebox.showwarning("Предупреждение", "Нет обработанного изображения для сохранения")
            return
        
        file_types = [
            ("PNG файлы", "*.png"),
            ("JPEG файлы", "*.jpg"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить обработанное изображение",
            defaultextension=".png",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Изображение сохранено: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
                self.status_var.set("Ошибка сохранения изображения")
    
    def reset_image(self):
        """Сбрасывает изображение к исходному состоянию."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Нет изображения для сброса")
            return
        
        self.processed_image = None
        self.processed_canvas.delete("all")
        self.processed_canvas.create_text(200, 150, text="Примените преобразование\nдля просмотра результата", 
                                        fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
        self.update_info("Изображение сброшено к исходному состоянию")
        self.status_var.set("Изображение сброшено к исходному состоянию")
    
    def on_transform_change(self, event=None):
        """Обрабатывает изменение типа преобразования."""
        transform_type = self.transform_var.get()
        
        descriptions = {
            "Логарифмическое": "Логарифмическое преобразование улучшает видимость деталей в темных областях изображения.",
            "Степенное": "Степенное преобразование позволяет регулировать контрастность изображения с помощью параметра гамма.",
            "Бинарное": "Бинарное преобразование создает черно-белое изображение на основе порогового значения.",
            "Вырезание диапазона яркостей": "Вырезание диапазона яркостей выделяет определенный диапазон яркостей в изображении."
        }
        
        self.desc_text.configure(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(1.0, descriptions.get(transform_type, ""))
        self.desc_text.configure(state=tk.DISABLED)
    
    def update_info(self, message):
        """Обновляет информационную панель."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, f"Информация об изображении:\n{message}")
        self.info_text.configure(state=tk.DISABLED)

def main():
    """Главная функция запуска приложения."""
    try:
        print("🚀 Запуск Photo Editor Pro...")
        print("✨ Современный интерфейс в стиле фоторедактора")
        print("🎨 Темная тема с акцентными цветами")
        print("🔄 Удобное сравнение до/после")
        print()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Создание приложения
        app = SimpleModernPhotoEditor(root)
        
        print("✅ Photo Editor Pro запущен успешно!")
        print("📝 Инструкции:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите тип преобразования в правой панели")
        print("   3. Нажмите '✨ Применить преобразование'")
        print("   4. Сохраните результат с помощью '💾 Сохранить'")
        print("   5. Используйте '🔄 Сброс' для возврата к исходному")
        print()
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

import pygame
import sys
import time

# تهيئة Pygame
pygame.init()

# أبعاد النافذة
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("عرض ثنائي الأبعاد (مطابقة الفريم الأصلي) باستخدام Pygame")

# الألوان
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)

background_image = pygame.image.load("360_F_283549444_QJP74KROpbcvsBvohYSSJxVfFIcqr5O8.jpg").convert()

scaled_background = pygame.transform.scale(background_image, (width, height))

# قراءة النقاط من الملف
lines_data = []
try:
    with open("AnimationFile.txt", 'r') as f:
        lines_data = f.readlines()
except FileNotFoundError:
    print("لم يتم العثور على ملف AnimationFile.txt. تأكد من وجود الملف في نفس المجلد.")
    sys.exit()

# نقاط الجسم ثلاثية الأبعاد (في البداية ستكون في مركز الشاشة)
body_points_3d = [[0, 0, 0] for _ in range(33)]

# اتصالات الخطوط بين النقاط (محدثة لتتوافق مع الصورة)
lines_connections = [
    (0, 2), (2, 7), (1, 3), (0, 5), (5, 8),(4, 6), # الرأس والعيون
    (0, 7), (0, 8), (7, 9), (8, 10), # الرأس والأذنين والفم
    (11, 12), # الرقبة والكتفين
    (11, 13), (13, 15), (15, 17), (17, 19), (19, 15), (15, 21), # الذراع الأيمن
    (12, 14), (14, 16), (16, 18), (18, 20), (20, 16), (16, 22), # الذراع الأيسر
    (11, 23), (12, 24), # الكتفين والوركين
    (23, 24), # الوركين
    (23, 25), (25, 27), (27, 29), (29, 31), (31, 27), # الساق اليمنى والقدم
    (24, 26), (26, 28), (28, 30), (30, 32), (32, 28)  # الساق اليسرى والقدم
]

counter = 0
clock = pygame.time.Clock() # للتحكم في معدل الإطارات

# دالة تحويل ثنائي الأبعاد من الفريم إلى النافذة (بدون منظور ثلاثي الأبعاد)
def project_2d_frame_to_window(point_3d):
    """يقوم بتحويل إحداثيات ثنائية الأبعاد من الفريم الأصلي إلى إحداثيات نافذة Pygame."""
    # 720, 1280
    x_3d, y_3d, z_3d = point_3d # لا نستخدم z بشكل مباشر في هذا التحويل
    frame_width = 1280  # افتراض عرض الفريم الأصلي (يمكن تعديله)
    frame_height = 720 # افتراض ارتفاع الفريم الأصلي (يمكن تعديله)

    scale_x = width / frame_width   # نسبة القياس الأفقية
    scale_y = height / frame_height  # نسبة القياس الرأسية

    x_2d = int(x_3d * scale_x)  # تطبيق القياس الأفقي
    y_2d = int(y_3d * scale_y)  # تطبيق القياس الرأسي

    return (x_2d, y_2d)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(scaled_background, (0, 0)) # ارسم الصورة في الزاوية العلوية اليسرى (0, 0)

    # screen.fill(black) # ملء الشاشة باللون الأسود في كل إطار

    try:
        points_str = lines_data[counter].strip().split(',')
        for i in range(33):
            x = float(points_str[0 + (i * 3)])  # استخدام x مباشرةً من البيانات
            y = float(points_str[1 + (i * 3)]) # استخدام y مباشرةً من البيانات
            z = float(points_str[2 + (i * 3)]) # لا نستخدم z في هذا التحويل، ولكن نحتفظ به في البيانات
            body_points_3d[i] = [x, y, z] # تخزين x, y, z الأصليين

        # رسم الخطوط
        for start_index, end_index in lines_connections:
            start_point_3d = body_points_3d[start_index]
            end_point_3d = body_points_3d[end_index]

            start_point_2d = project_2d_frame_to_window(start_point_3d) # استخدام دالة التحويل الجديدة
            end_point_2d = project_2d_frame_to_window(end_point_3d)   # استخدام دالة التحويل الجديدة

            pygame.draw.line(screen, green, start_point_2d, end_point_2d, 3)

        # رسم النقاط كدوائر صغيرة (اختياري)
        for point_3d in body_points_3d:
            point_2d = project_2d_frame_to_window(point_3d) # استخدام دالة التحويل الجديدة
            pygame.draw.circle(screen, white, point_2d, 3) # دوائر بيضاء صغيرة
        
        pygame.draw.circle(screen, (255, 0, 0),project_2d_frame_to_window(body_points_3d[0]), 40) # رسم النقطة الأولى بحجم أكبر

        counter += 1
        if counter == len(lines_data):
            counter = 0

    except IndexError:
        print("تم الوصول إلى نهاية ملف الرسوم المتحركة.")
        running = False # إيقاف الحلقة عند النهاية

    pygame.display.flip() # تحديث الشاشة لعرض الرسومات
    clock.tick(30) # تحديد معدل الإطارات إلى 30 إطار في الثانية

pygame.quit()
sys.exit()
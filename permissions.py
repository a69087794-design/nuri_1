# Foydalanuvchi turlari (Konstantalar)
ADMIN = "admin"
USER = "user"
STRANGER = "stranger"

class PermissionManager:
    def __init__(self):
        # Ruxsatlar ierarxiyasi
        self.PERMISSIONS = {
            ADMIN: ["all"],
            USER: [
                "internet", "ping", "ip",       # network_module
                "brauzer", "sayt", "qidir",     # browser_module
                "yangilik", "habar",            # news_module
                "youtube", "yutub",             # youtube_module
                "savol", "ai"                   # ai_engine uchun umumiy suhbat
            ],
            STRANGER: [
                "parol", "login"                # Stranger faqat tizimga kira oladi
            ]
        }
        
        # Vaqtinchalik foydalanuvchilar (Xotira yoki SQLite yuklanmaguncha kesh sifatida)
        self.users = {
            "admin": {"role": ADMIN, "allowed_apps": ["all"]},
            "root": {"role": ADMIN, "allowed_apps": ["all"]}
        }

    def get_role(self, username: str) -> str:
        """Foydalanuvchi nomiga qarab uning rolini qaytaradi"""
        if username in self.users:
            return self.users[username]["role"]
        return STRANGER

    def check_access(self, current_role: str, command: str) -> bool:
        """
        Kiritilgan buyruq va foydalanuvchi roliga qarab ruxsatni tekshiradi.
        Main.py dagi tartib bilan to'liq mos keladi.
        """
        # Admin barcha narsaga ruxsatga ega
        if current_role == ADMIN:
            return True
            
        perms = self.PERMISSIONS.get(current_role, [])
        
        # Agar ruxsatlar ro'yxatidagi biror so'z buyruq ichida bo'lsa, ruxsat beriladi
        for trigger in perms:
            if trigger in command:
                return True
                
        return False

    def add_user(self, username: str, role: str, allowed_apps: list = []):
        """Yangi foydalanuvchi qo'shish (Faqat admin tomonidan)"""
        if role in [ADMIN, USER, STRANGER]:
            self.users[username] = {
                "role": role,
                "allowed_apps": allowed_apps
            }

    def remove_user(self, username: str):
        """Foydalanuvchini o'chirish (Faqat admin tomonidan)"""
        if username in self.users:
            del self.users[username]

    def get_denied_message(self) -> str:
        """Ruxsat berilmaganda qaytadigan matn"""
        return "Kechirasiz, ushbu buyruqni bajarish uchun ruxsatingiz yetarli emas."

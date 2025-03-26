import argparse
import time
import random
from selenium.webdriver.common.by import By

from browser_automation import BrowserManager, Node
from utils import Utility
from google import Auto as GoogleAuto
from google import Setup as GoogleSetup

QUESTIONS = [
    "What is artificial intelligence?",
    "How does machine learning work?",
    "What are the benefits of automation?",
    "Can you explain blockchain technology?",
    "What is cloud computing?",
    "How does cybersecurity work?",
    "What is the future of technology?",
    "How do neural networks function?",
    "What is quantum computing?",
    "How does data science work?",
    "What are the applications of IoT?",
    "How does virtual reality work?",
    "What is augmented reality?",
    "How does 5G technology work?",
    "What is edge computing?",
    "How does robotics work?",
    "What is natural language processing?",
    "How does computer vision work?",
    "What is deep learning?",
    "How does big data work?",
    "What is the role of AI in healthcare?",
    "How does autonomous driving work?",
    "What is smart home technology?",
    "How does renewable energy work?",
    "What is sustainable technology?",
    "How does digital transformation work?",
    "What is the future of work?",
    "How does remote work technology work?",
    "What is digital marketing?",
    "How does social media work?",
    "What is e-commerce?",
    "How does online payment work?",
    "What is digital banking?",
    "How does cryptocurrency work?",
    "What is fintech?",
    "How does mobile banking work?",
    "What is digital identity?",
    "How does biometric authentication work?",
    "What is cloud storage?",
    "How does data backup work?",
    "What is network security?",
    "How does encryption work?",
    "What is digital privacy?",
    "How does password protection work?",
    "What is two-factor authentication?",
    "How does VPN work?",
    "What is firewall protection?",
    "How does antivirus software work?",
    "What is malware protection?",
    "How does phishing protection work?",
    "What is ransomware protection?",
    "How does data recovery work?",
    "What is system optimization?",
    "How does computer maintenance work?",
    "What is software development?",
    "How does coding work?",
    "What is web development?",
    "How does mobile app development work?",
    "What is game development?",
    "How does UI/UX design work?",
    "What is responsive design?",
    "How does cross-platform development work?",
    "What is agile methodology?",
    "How does project management work?",
    "What is quality assurance?",
    "How does testing work?",
    "What is continuous integration?",
    "How does DevOps work?",
    "What is containerization?",
    "How does Docker work?",
    "What is Kubernetes?",
    "How does microservices work?",
    "What is API development?",
    "How does REST API work?",
    "What is GraphQL?",
    "How does WebSocket work?",
    "What is real-time communication?",
    "How does streaming work?",
    "What is content delivery?",
    "How does CDN work?",
    "What is load balancing?",
    "How does scaling work?",
    "What is high availability?",
    "How does disaster recovery work?",
    "What is business continuity?",
    "How does risk management work?",
    "What is compliance?",
    "How does data governance work?",
]

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.node = node
        self.driver = node._driver
        self.google = GoogleAuto(node, profile)
        self.profile_name = profile.get('profile_name')
        self.email = profile.get('email')

    def login_klokapp(self):
        self.node.go_to('https://klokapp.ai/?referral_code=2AQB2MK6')
        
        # Đăng nhập Klokapp
        if not self.node.find(By.XPATH, '//div[text()="Total Mira Points"]'):
            self.node.log('🔄 Đang thực hiện đăng nhập Klokapp...')
            
            # Đợi và click nút đăng nhập với Google
            if not self.node.find_and_click(By.XPATH, '//button[text()="Continue with Google"]'):
                self.node.snapshot('Không tìm thấy nút "Continue with Google"')
                return
            
            # chuyển tab đến Google cho lần đầu kết nối
            if self.node.switch_tab('https://accounts.google.com/'):
                if not self.node.find_and_click(By.CSS_SELECTOR, f'div[data-email="{self.email}"]'):
                    self.node.snapshot('Không tìm thấy email Google')
                    return
                
                # Tìm nút tiếp tục bằng nhiều cách khác nhau
                buttons = self.node.find_all(By.CSS_SELECTOR, 'button[type="button"]')
                if len(buttons) >= 2:
                    continue_button = buttons[1]  # Lấy button thứ 2 (index 1)
                    if continue_button.is_displayed():
                        continue_button.click()
                        self.node.log('✅ Đã nhấn nút tiếp tục')
                    else:
                        self.node.snapshot('Nút tiếp tục không hiển thị')
                        return
                else:
                    self.node.snapshot('Không tìm thấy đủ button')
                    return

                self.node.switch_tab('https://klokapp.ai/app')

            # Kiểm tra có popup Close và Let’s go!    
            self.node.find_and_click(By.XPATH, '//button[text()="Let’s go!"]', timeout=15)        
            self.node.find_and_click(By.XPATH, '//button[text()="Close"]', timeout=15)        

            if not self.node.find(By.XPATH, '//div[text()="Total Mira Points"]'):
                self.node.snapshot('Không thể xác nhận đăng nhập Klokapp thành công')
                return
            
        return True
    
    def chat_ai(self, message: str):
        # Vòng lặp gửi tin nhắn
        if not self.node.find_and_input(By.CSS_SELECTOR, 'textarea', message, delay=0.1):
            self.node.snapshot('Không tìm thấy ô nhập tin nhắn')
            return False
        if not self.node.press_key('Enter'):
            self.node.snapshot('Không thể nhấn nút Enter')
            return False
        
        # trong vòng 5p nên dừng lại, chứ không phải True while quài
        start_time = time.time()
        while True:
            if time.time() - start_time > 300:
                self.node.log('👋 Kết thúc chat')
                break
            
            # Kiểm tra nút gửi có bị disabled không bằng cách kiểm tra opacity
            send_button = self.node.find(By.CSS_SELECTOR, 'button[type="submit"] img', show_log=False)
            if send_button:
                opacity = send_button.get_attribute('class')
                if 'opacity-40' in opacity:
                    self.node.log('⏳ Đang đợi AI trả lời...')
                    Utility.wait_time(2)  # Đợi 2 giây rồi kiểm tra lại
                    continue
                elif 'opacity-100' in opacity:
                    
                    return True
            else:
                return False
                
        return False
    
    def _run(self):
        # Thực hiện đăng nhập Google trước
        self.google._run()
            
        # Sau khi đăng nhập Google thành công, tiếp tục task khác
        self.login_klokapp()
        while True:
            text = self.node.get_text(By.XPATH, '//div[div[text()="of 10 prompts used"]]//div')
            if text:
                if text.startswith('10'):
                    self.node.snapshot('Đã sử dụng hết 10 lần')
                    break
                else:
                    self.chat_ai(random.choice(QUESTIONS))
            else:
                self.node.snapshot('Không tìm thấy text')
                break


class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        self.google = GoogleSetup(node, profile)
        
    def _run(self):
        self.google._run()
        self.node.new_tab('https://klokapp.ai/?referral_code=2AQB2MK6')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.get_data('profile_name', 'email', 'password')
    if not profiles:
        print("Không có dữ liệu để chạy")
        exit()

    browser_manager = BrowserManager(AutoHandlerClass=Auto, SetupHandlerClass=Setup)
    browser_manager.config_extension('meta-wallet-*.crx')
    browser_manager.run_terminal(
        profiles=profiles,
        max_concurrent_profiles=4,
        block_media=True,
        auto=args.auto,
        headless=args.headless,
        disable_gpu=args.disable_gpu,
    )
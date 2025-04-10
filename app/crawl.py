import requests                      # Thư viện gửi yêu cầu HTTP để lấy dữ liệu từ trang web
from bs4 import BeautifulSoup       # Thư viện để phân tích và trích xuất dữ liệu từ HTML

def crawl_a():  # Định nghĩa hàm crawl_a dùng để thu thập dữ liệu từ chuyên mục AI
    url = "https://vnexpress.net/cong-nghe/ai"     # Địa chỉ trang chuyên mục AI của VnExpress
    headers = {'User-Agent': 'Mozilla/5.0'}        # Thêm thông tin User-Agent để giả lập trình duyệt, tránh bị chặn

    res = requests.get(url, headers=headers)       # Gửi yêu cầu GET để lấy nội dung trang web
    soup = BeautifulSoup(res.text, 'html.parser')  # Dùng BeautifulSoup để phân tích HTML trả về

    articles = []   # Tạo danh sách rỗng để lưu các bài viết sau khi thu thập

    for i, item in enumerate(soup.select("article.item-news")[:5], 1):  # Duyệt qua 5 bài viết đầu tiên trong danh sách
        title_tag = item.find(['h2', 'h3'], class_='title-news')        # Tìm thẻ tiêu đề bài viết (h2 hoặc h3 có class 'title-news')
        if title_tag and title_tag.a:  # Nếu tìm được thẻ tiêu đề và có thẻ <a> chứa liên kết bài viết
            try:
                article_url = title_tag.a.get('href').strip()    # Lấy URL bài viết và loại bỏ khoảng trắng
                article_res = requests.get(article_url, headers=headers)  # Gửi yêu cầu GET đến trang bài viết
                article_soup = BeautifulSoup(article_res.text, 'html.parser')  # Phân tích HTML của bài viết

                time_tag = article_soup.find('span', class_='date') or article_soup.find('span', class_='time')  
                # Tìm thời gian đăng bài, có thể nằm trong thẻ 'date' hoặc 'time'

                author_tag = article_soup.find('p', class_='Normal', attrs={'style': 'text-align:right;'})  
                # Tìm tên tác giả trong thẻ <p> có style căn phải (thường là cuối bài)

                article_data = {   # Tạo một dictionary chứa thông tin của bài viết
                    "title": title_tag.a.get('title', '').strip(),             # Tiêu đề bài viết
                    "url": article_url,                                        # Đường dẫn bài viết
                    "summary": item.p.text.strip() if item.p else '',          # Tóm tắt bài viết (nếu có)
                    "time": time_tag.text.strip() if time_tag else '',         # Thời gian đăng (nếu tìm thấy)
                    "author": author_tag.text.strip() if author_tag else ''    # Tác giả (nếu tìm thấy)
                }
                articles.append(article_data)   # Thêm thông tin bài viết vào danh sách kết quả

            except Exception as e:  # Nếu xảy ra lỗi khi xử lý bài viết
                articles.append({   # Thêm thông tin lỗi vào danh sách để dễ kiểm tra
                    "title": f"BÀI {i}: LỖI khi xử lý bài viết",
                    "error": str(e)
                })

    return articles  # Trả về danh sách các bài viết đã thu thập (hoặc thông báo lỗi)
if __name__ == "__main__":  # Khi chạy trực tiếp tệp này (không phải khi import)
    data = crawl_a()  # Gọi hàm crawl_a để lấy danh sách bài viết

    for i, article in enumerate(data, 1):  # Duyệt qua từng bài viết để in thông tin ra màn hình
        print(f"\n===>TIÊU ĐỀ {i}: {article.get('title', '')}")       # In tiêu đề bài viết
        print(f"URL: {article.get('url', '')}")                       # In đường dẫn bài viết
        print(f"TÓM TẮT: {article.get('summary', '')}")              # In đoạn tóm tắt
        print(f"THỜI GIAN: {article.get('time', '')}")               # In thời gian đăng bài
        print(f"TÁC GIẢ: {article.get('author', '')}")              # In tên tác giả
        if 'error' in article:                                       # Nếu có lỗi, in lỗi ra
            print(f"LỖI: {article['error']}")

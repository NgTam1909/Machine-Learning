const delay = ms => new Promise(res => setTimeout(res, ms));
const main = async () => {
    try {
        const data = [];
        const store = []
        let totalComments = 0
        // tìm và chọn menu chọn sắp xếp bình luận
        console.log("Chọn menu sắp xếp bình luận");
        const menuSelect = document.querySelector('div[aria-haspopup="menu"]')
        console.log("Chọn tất cả bình luận");
        menuSelect.click()
        await delay(1000)
        const listMenuItem = [...document.querySelectorAll('div[role="menuitem"]')]
        // chọn mục bình luận mới nhất
        listMenuItem.at(-1).click()
        // chờ 2s cho trang load lại bình luận mới nhất
        await delay(2000)
        const [, menu, ...other] = [...document.querySelector('div[role="dialog"] > div > div > div').children]
        // mỗi 100ms kiểm tra có loading hay không
        const inverval = setInterval(async () => {
            menu.scrollTo({
                top: menu.scrollHeight + 100,
                behavior: 'smooth'
            });
            const listComments = [...document.querySelectorAll(
                'div.x1r8uery.x1iyjqo2.x6ikm8r.x10wlt62.xv54qhq > div:nth-child(1) > div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz > div > div'
            )];
            const loading = document.querySelector('div[data-visualcompletion="loading-state"]')
            // nếu load xong toàn bộ comment
            if (loading == null && totalComments != listComments.length) {
                console.log(store);
                clearInterval(inverval)
            }
            totalComments += listComments.length
            for (const element of listComments) {
                const [spanElementFullname, otherElement] = element.children
                const tagA = spanElementFullname.querySelector('a')
                if (!tagA) continue;
                const params = new URL(tagA.href).searchParams;
                const commentId = params.get("comment_id");
                if (data.includes(commentId)) continue;
                const full_name = spanElementFullname.textContent
                const comment = otherElement?.textContent.trim() || ""
                //  Bỏ qua comment chỉ tag tên
                const onlyTag = otherElement 
                    && otherElement.children.length > 0 
                    && [...otherElement.children].every(child => child.tagName === "A")
                    && comment.split(/\s+/).length === otherElement.children.length
                if (onlyTag || comment === "") continue;
                data.push(commentId)
                store.push({ full_name, comment })
            }
            console.log(`Đã lấy được ${data.length} bình luận`);
        }, 100)
    } catch (error) {
        console.log(error);
    }
}
main()


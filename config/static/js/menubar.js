var startPos = 0, winScrollTop = 0;
// scrollイベントを設定
window.addEventListener('scroll', function () {
    winScrollTop = this.scrollY;
    if (winScrollTop >= startPos) {
        // 下にスクロールされた時
        if (winScrollTop >= 10) {
            // 下に10pxスクロールされたら隠す
            document.getElementById('nav-menu').classList.add('hide');
        }
    } else {
        // 上にスクロールされた時
        document.getElementById('nav-menu').classList.remove('hide');
    }
    startPos = winScrollTop;
});
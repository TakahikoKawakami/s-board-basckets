class CookieUtil {
    static getCookeiArray() {
        let result = new Array;
        if (document.cookie != '') {
            for (data of document.cookie) {
                result = data;
            }
        }
        return result;
    }
}

export default CookieUtil;
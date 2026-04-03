(function () {
  var _f = window.fetch;
  window.fetch = function (url, opts) {
    if (typeof url === "string" && url.indexOf(".tar.gz") !== -1) {
      return _f(url, opts).then(function (resp) {
        var total = parseInt(resp.headers.get("Content-Length") || "0", 10);
        var loaded = 0;
        var sEl = document.getElementById("status");
        var pEl = document.getElementById("progress");
        if (sEl) sEl.innerText = "Downloading... 0%";
        if (pEl) { pEl.max = 100; pEl.value = 0; }
        var reader = resp.body.getReader();
        var chunks = [];
        function pump() {
          return reader.read().then(function (r) {
            if (r.done) {
              if (sEl) sEl.innerText = "Extracting...";
              if (pEl) pEl.value = 100;
              return new Response(new Blob(chunks), { status: resp.status, headers: resp.headers });
            }
            chunks.push(r.value);
            loaded += r.value.length;
            if (total) {
              var pct = Math.min(99, Math.round(loaded / total * 100));
              if (sEl) sEl.innerText = "Downloading... " + pct + "%";
              if (pEl) pEl.value = pct;
            }
            return pump();
          });
        }
        return pump();
      });
    }
    return _f(url, opts);
  };
})();

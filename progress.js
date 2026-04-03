(function () {
  var _f = window.fetch;
  window.fetch = function (url, opts) {
    if (typeof url === "string" && url.indexOf(".tar.gz") !== -1) {
      return _f(url, opts).then(function (resp) {
        var total = parseInt(resp.headers.get("Content-Length") || "0", 10);
        var loaded = 0;

        // #transfer is hidden by Python startup code; show it again for progress
        var transferEl = document.getElementById("transfer");
        var sEl = document.getElementById("status");
        var pEl = document.getElementById("progress");
        var infoEl = document.getElementById("infobox");

        if (transferEl) transferEl.hidden = false;
        if (pEl) { pEl.max = 100; pEl.value = 0; }

        function setMsg(text) {
          if (sEl) sEl.innerText = text;
          if (infoEl) infoEl.innerText = text;
        }
        setMsg("Downloading game assets... 0%");

        var reader = resp.body.getReader();
        var chunks = [];
        function pump() {
          return reader.read().then(function (r) {
            if (r.done) {
              setMsg("Extracting game assets...");
              if (pEl) pEl.value = 100;
              return new Response(new Blob(chunks), { status: resp.status, headers: resp.headers });
            }
            chunks.push(r.value);
            loaded += r.value.length;
            if (total) {
              var pct = Math.min(99, Math.round(loaded / total * 100));
              setMsg("Downloading game assets... " + pct + "%");
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

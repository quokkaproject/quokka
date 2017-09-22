var github = (function(){
  function escapeHtml(str) {
    return $('<div/>').text(str).html();
  }
  function render(target, repos){
    var i = 0, fragment = '', t = $(target)[0];
    fragment += '<ul class="list-group" id="github">';

    for(i = 0; i < repos.length; i++) {
      fragment += '<li class="list-group-item"><a href="'+repos[i].html_url+'">'+repos[i].name+'</a><p><small>'+escapeHtml(repos[i].description||'')+'</small></p></li>';
    }
    fragment += '</ul>';
    t.innerHTML = fragment;
  }
  return {
    showRepos: function(options){
      $.ajax({
          url: "https://api.github.com/users/"+options.user+"/repos?callback=?"
        , dataType: 'jsonp'
        , error: function (err) { $(options.target + ' li.loading').addClass('error').text("Error loading feed"); }
        , success: function(data) {
          var repos = [];
          if (!data || !data.data) { return; }
          for (var i = 0; i < data.data.length; i++) {
            if (options.skip_forks && data.data[i].fork) { continue; }
            repos.push(data.data[i]);
          }
          repos.sort(function(a, b) {
            var aDate = new Date(a.pushed_at).valueOf(),
                bDate = new Date(b.pushed_at).valueOf();

            if (aDate === bDate) { return 0; }
            return aDate > bDate ? -1 : 1;
          });

          if (options.count) { repos.splice(options.count); }
          render(options.target, repos);
        }
      });
    }
  };
})();

$(document).ready(function () {
  $('#sendButton').on('click', function () {
    getBotResponse();
  });

  $('#textInput').keypress(function (e) {
    if (e.which == 13) {
      getBotResponse();
    }
  });

  function scrollToBottom() {
    var chatbox = document.getElementById('chatbox');
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function getBotResponse() {
    var rawText = $('#textInput').val().trim();
    if (!rawText) return;

    var userHtml =
      '<div class="message user-message"><span>' + rawText + '</span></div>';
    $('#textInput').val('');
    $('#chatbox').append(userHtml);

    scrollToBottom();

    var loadingHtml =
      '<div class="message bot-message loading"><span class="dot-1"></span><span class="dot-2"></span><span class="dot-3"></span> Loading</div>';
    $('#chatbox').append(loadingHtml);

    scrollToBottom();

    $.get('/get', { msg: rawText }).done(function (data) {
      $('.loading').remove();
      var botHtml =
        '<div class="message bot-message"><span>' + data + '</span></div>';
      $('#chatbox').append(botHtml);

      scrollToBottom();
    });
  }
});

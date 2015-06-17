
function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

var soundId = localStorage.getItem("soundId");

if ( soundId === null) {
    soundId = guid();
    localStorage.setItem("soundId", soundId);
}

module.exports = soundId;

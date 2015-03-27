var all_btn, elem, get_result, input_value, tokens, reset_values, set_event, operator, add_digit, _i, _len;

input_value = [];
tokens = [];

set_event = function(elem) {
  if (elem.hasClass("num")) {
    return elem.on("click", function() {
      input_value.push(elem.val().replace(',','.'));
      return $(".calc_input").val(tokens.join("").replace('.',',')+input_value.join("").replace('.',','));
    });
  } else if (elem.hasClass("operator")) {
    return elem.on("click", function() {
      return operator(elem);
    });
  } else if (elem.hasClass("reset")) {
    return elem.on("click", function() {
      return reset_values(false);
    });
  }
};

all_btn = $(".btn");

for (_i = 0, _len = all_btn.length; _i < _len; _i++) {
  elem = all_btn[_i];
  set_event($(elem));
}

$(".result").on("click", function() {
  return get_result(tokens);
});

$(".sep").on("click", function() {
  return $(".sep").prop("disabled", true);
});

$(".revert").on("click", function() {
  if (input_value[0] === "-") {
    input_value.shift();
  } else {
    input_value.unshift("-");
  }
  return $(".calc_input").val(tokens.join("").replace('.',',')+input_value.join("").replace('.',','));
});

operator = function(elem) {
  if (elem == null) {
    elem = void 0;
  }
	add_digit();
	tokens.push(elem.val());
  $(".calc_input").val(tokens.join("").replace('.',','));
  input_value = [];
  return $(".sep").prop("disabled", false);
  
};

reset_values = function(state) {
  input_value = [];
  tokens = []
  $(".calc_input").val("")
};


add_digit = function() {

if (input_value.length > 0) {
  	token = input_value.join("").replace(',','.')
  	tokens.push(token)
    }
};
get_result = function(t) {
	add_digit();
  	return $.ajax({
    	"type": "POST",
    	"url": "/api/calc",
    	"data": {
      		"tokens": tokens,
    	}
  	}).done(function(r) {
  if ("error" in r) {
  	$(".calc_msg").val(r.error)
  };
  if ("response" in r) {
      tokens = [];
    $(".calc_input").val(r.response);
    input_value = [r.response];
  };
   return $(".sep").prop("disabled", false);
  });
};

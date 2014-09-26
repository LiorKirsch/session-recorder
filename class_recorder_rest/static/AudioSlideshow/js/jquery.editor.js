(function ($) {
  
	$.fn.image_editor = function(options) {
      
		var settings = {
			jPlayerPath: "/lib/swf",
			suppliedFileType: "mp3",
			playSelector: ".audio-play",
			pauseSelector: ".audio-pause",
			currentTimeSelector: ".play-time",
			durationSelector: ".total-time",
			playheadSelector: ".playhead",
			timelineSelector: ".timeline",
			data_audio: "",
			data_audio_duration: "",
            all_data: ""
		};
	  
		if (options) {
            jQuery.extend(settings, options);
		}
		
		// Begin to iterate over the jQuery collection that the method was called on
		return this.each(function () {
		  
			// Cache `this`
			var $that = $(this),
				$slides = $that.find('.audio-slides').children(),
				
				$currentTime = $that.find(settings.currentTimeSelector),
				$duration = $that.find(settings.durationSelector),
				$playhead = $that.find(settings.playheadSelector),
				$timeline = $that.find(settings.timelineSelector),
				$playButton = $that.find(settings.playSelector),
				$pauseButton = $that.find(settings.pauseSelector),

				slidesCount = $slides.length,
				slideTimes = [],
				audioDurationinSeconds = parseInt(settings.data_audio_duration),
				isPlaying = false,
				currentSlide = -1;

			$pauseButton.hide();
				
			// Setup slides			
			$slides.each(function (index, el) {
				var $el = $(el);
				$el.hide();

				var second = parseInt($el.attr('data-slide-time')),
					thumbnail = $el.attr('data-thumbnail');
				
				
                slideTimes.push(second);


                var $thumb_img = $('<img src="' + thumbnail + '">'),
                    $remove_button = $('<i class="icon-large  icon-minus-sign"></i>'),
                    $imgSpan = $('<span>').append($thumb_img).append($remove_button),
                    $marker = $('<a href="javascript:;" class="marker" data-time="' + second + '"> </a>').append($imgSpan),
                    $marker_container = $('<div>').append($marker),
                    l = (second  / audioDurationinSeconds) * 100 + '%';


                $marker_container.draggable({
                    axis: "x",
//                    containment: "parent",
                    stop: function (event, ui) {
                        /* Update the location of the marker */
                        var l = ( 100 * parseFloat($(this).css("left")) / parseFloat($(this).parent().css("width")) )+ "%" ;
                        $(this).css("left" , l);
                    }
                });

                $marker_container.css('left',l);
                $marker.data('index',index);
                $marker.click(function(e){
                    var current_marker_index = $(this).data('index') ;
//                    console.log('clicked on ' + current_marker_index );
                    setAudioSlide(current_marker_index);
//                    $jPlayerObj.jPlayer("play", parseInt($(this).attr('data-time')) + .5);
                });

                $remove_button.click(function(e){
                    if (this.isClosed)
                    {
                        var parent_element = $(this).parent().parent();
                        parent_element.css('opacity','1');
                        parent_element.css('z-index', parseInt(parent_element.css('z-index')) + 10);
                        $(this).removeClass('icon-plus-sign') ;
                        $(this).addClass('icon-minus-sign') ;
                        this.isClosed = false;
                    }
                    else
                    {
                        var parent_element = $(this).parent().parent();
                        parent_element.css('opacity','0.3');
                        parent_element.css('z-index',  parseInt(parent_element.css('z-index')) - 10);
                        $(this).removeClass('icon-minus-sign') ;
                        $(this).addClass('icon-plus-sign') ;
                        this.isClosed = true;
                    }
                });
                
                $timeline.append($marker_container);
                
				if(index == 0){
                    $marker_container.css('left','1%');
                }
			});

			var $jPlayerObj = $('<div></div>');
			$that.append($jPlayerObj);
		
			$jPlayerObj.jPlayer({
				ready: function () {
					$.jPlayer.timeFormat.padMin = false;
					$(this).jPlayer("setMedia", {
						mp3: settings.data_audio
					});
				},
				swfPath: settings.jPlayerPath,
				supplied: settings.suppliedFileType,
				preload: 'auto',
				cssSelectorAncestor: ""
			});
				
			$jPlayerObj.bind($.jPlayer.event.timeupdate, function(event) { // Add a listener to report the time play began
				var curTime = event.jPlayer.status.currentTime;
				audioDurationinSeconds = event.jPlayer.status.duration;
				var p = (curTime / audioDurationinSeconds) * 100 + "%";

				$currentTime.text($.jPlayer.convertTime(curTime));
				$duration.text($.jPlayer.convertTime(audioDurationinSeconds));

				$playhead.width(p);

				if (slidesCount){
					var nxtSlide = 0;
					for (var i = 0; i < slidesCount; i++) {
						if(slideTimes[i] < curTime){
							nxtSlide = i + 1;
						}
					}

					setAudioSlide(nxtSlide);
				}
			});
				
			$jPlayerObj.bind($.jPlayer.event.play, function(event) { // Add a listener to report the time play began
				isPlaying = true;
				$playButton.hide();
				$pauseButton.show();
			});
			
			$jPlayerObj.bind($.jPlayer.event.pause, function(event) { // Add a listener to report the time pause began
				isPlaying = false;
				$pauseButton.hide();
				$playButton.show();
			});
			
			$slides.click(function(event){
				$jPlayerObj.jPlayer("play");
			});
			
			$playButton.click(function(event){
				$jPlayerObj.jPlayer("play");
			});
				
			$pauseButton.click(function(event){
				$jPlayerObj.jPlayer("pause");
			});
			
			$timeline.click(function(event){
				var l = event.pageX -  $timeline.offset().left;
				var t = (l / $timeline.width()) * audioDurationinSeconds;

				$jPlayerObj.jPlayer("play", t);
			});
			
			setAudioSlide(0);
			
			function setAudioSlide(n){
				if(n != currentSlide){
					if($slides.get(currentSlide)){
						$($slides.get(currentSlide)).fadeOut();
					}

					$($slides.get(n)).fadeIn();
					currentSlide = n;
				}
			}
				
		});
	};
}(jQuery));
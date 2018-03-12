var hiddenClass = 'hidden';
var shownClass = 'toggled-from-hidden';

function sectionHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === hiddenClass) {
            child.className = shownClass;
        }
    }
}

function sectionEndHover() {
    var children = this.children;
    for(var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.className === shownClass) {
            child.className = hiddenClass;
        }
    }
}

(function() {
    var allSections = document.getElementsByClassName('hoversection');
    for(var i = 0; i < allSections.length; i++) {
        allSections[i].addEventListener('mouseover', sectionHover);
        allSections[i].addEventListener('mouseout', sectionEndHover);
    }
}());

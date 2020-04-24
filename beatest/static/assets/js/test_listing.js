$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});
Number.prototype.round = function (p) {
    p = p || 10;
    return parseFloat(this.toFixed(p));
}
// document.querySelectorAll("#mock, #topic, #section")
// document.addEventListener('click', handleClickEvents, false)
// function handleClickEvents(evt) {
//     myEventTarget = evt.target;
//     if (myEventTarget.id === 'mock') {
//         let myObj = obj.filter(function (n) {
//             return n.character === "Mock";
//         })
//         document.getElementById("main_listing").innerHTML = template(myObj);
//     }
//     else if (myEventTarget.id === 'topic') {
//         let myObj = obj.filter(function (n) {
//             return n.character === "Topic";
//         })
//         document.getElementById("main_listing").innerHTML = template(myObj);
//     }
//     else if (myEventTarget.id === 'section') {
//         let myObj = obj.filter(function (n) {
//             return n.character === "Section";
//         })
//         document.getElementById("main_listing").innerHTML = template(myObj);
//     }
// }
// document.getElementById('completed').addEventListener('change', handleCompleted, false)
// function handleCompleted() {
//     if (this.checked) {
//         let myObj = obj.filter(function (n) {
//             return n.is_complete === true;
//         })
//         document.getElementById("main_listing").innerHTML = template(myObj);
//     }
// };
// document.querySelectorAll("#paid, #free")
// document.addEventListener('click', handleSecondClickEvents, false)
// function handleSecondClickEvents(evt) {
//     myEventTarget = evt.target;
//     if (myEventTarget.id === 'free') {
//         // filter.character = "Mock";
//         let myObj = obj.filter(function (n) {
//             return n.price === 0;
//         })
//         document.getElementById("main_listing").innerHTML = template(myObj);
//     }
//     else if (myEventTarget.id === 'paid') {
//         // filter.character = "Mock";
//         let myObj = obj.filter(function (n) {
//             return n.price > 0;
//         })
//         document.getElementById("main_listing").innerHTML = template(myObj);
//     }
// }
// var Shuffle = window.Shuffle;

// var element = document.querySelector('.test_listing');
// // var sizer = element.querySelector('.my-sizer-element');

// var shuffleInstance = new Shuffle(element, {
//     itemSelector: '.card',
//     // sizer: sizer // could also be a selector: '.my-sizer-element'
// });

// shuffleInstance.filter(['mock', 'topic']);

// shuffleInstance.filter(function (element) {
//     return element.character === "Mock";
// });
// Demo.prototype.addSearchFilter = function () {
//     return document.querySelector('.character').addEventListener('click', this._handleSearchKeyup.bind(this));
// };

// // Filter the shuffle instance by items with a title that matches the search input.
// Demo.prototype._handleSearchKeyup = function (evt) {
//     var searchText = evt.target.value();

//     this.shuffle.filter(function (element, shuffle) {
//         var titleElement = element.querySelector('.card');
//         var titleText = titleElement.textContent.toLowerCase().trim();

//         return titleText.indexOf(searchText) !== -1;
//     });
// };



var Shuffle = window.Shuffle;
var element = document.querySelector('.test_listing');
var shuffleInstance = new Shuffle(element, {
    itemSelector: '.test-card',
    isCentered: true,
});

// todo maintain a dictionary specifying the state of filters

// every time this state is updated

// shuffleInstance should be updated
var filters = {
    characterClicked: false,
    priceClicked: false,
    completedChecked: false
};

document.querySelectorAll('#mock, #topic, #section')
document.querySelectorAll('#paid, #free')
document.querySelectorAll('#completed')
document.addEventListener('click', handleClickEvent, false)
document.addEventListener('change', handleChangeEvent, false)

function handleClickEvent(evt) {
    myEventTarget = evt.target;
    if (myEventTarget.id === 'mock' || myEventTarget.idm === "topic" || myEventTarget.id === 'section') {
        return filters.characterClicked = true;
    }
    if (myEventTarget.id === 'paid' || myEventTarget.id === 'free') {
        return filters.priceClicked = true;
    }
}
function handleChangeEvent(evt) {
    myEventTarget = evt.target;
    if (myEventTarget.checked) {
        return filters.completedChecked = true
    }
}

function handleFilterEvent(evt) {
    console.log(evt)
    shuffleInstance.filter(function (element) {
        console.log(element.getAttribute('data-json'));
        let json = JSON.parse(element.getAttribute('data-json'));
        return json.character === "Mock";
    });
};

shuffleInstance.update();

// function template(obj) {
//     return `${obj.map(function (data) {
//         return `
//     <div class="card" style="width: 18rem;">
//     <img src="assets/img/recognition/scoopearth.png" class="card-img-top" alt="...">
//     <div class="card-body">
//     <h5 class="card-title">${data.name}</h5>
//     <div class="card_info">
//         <div class="new-data row">
//         <div class="col">${(data.total_time / 3600).round(3)}</div>
//         <div class="col">${data.section_count}</div>
//         <div class="col">${data.quesiton_count}</div>

//         </div>
//         <div class="row">
//             <div class="col">
//                 Hours
//             </div>
//             <div class="col">
//                 sections
//             </div>
//             <div class="col">
//                 Questions
//             </div>
//         </div>
//     </div>

//     <a href="#" class="btn btn-primary">Start</a>
//     </div>
//     </div>`
//     }).join('')}
//     </div>
//     </div>
//     `
// }

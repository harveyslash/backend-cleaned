// THIS IS 
//         EDUCATION LOGIC
var educations = [
    {
        id: 1,
        type: "Schools",
        institution: "Modern",
        to: "2019-05-15",
        from: "2019-05-15"
    },
    {
        id: 2,
        type: "Schools",
        institution: "Don Bosco",
        to: "2019-05-15",
        from: "2019-05-15"
    }
];
$.each(educations, function (i, education) {
    appendToEduTable(education);
});
$("form").submit(function (e) {
    e.preventDefault();
});
$("form#addEducation").submit(function () {
    msg = "education has been added"
    var education = {};
    var lastEducation;
    var typeInput = $('input[name="type"]').val().trim();
    var institutionInput = $('input[name="institution"]').val().trim();
    var fromInput = $('input[name="from"]').val().trim();
    var toInput = $('input[name="to"]').val().trim();
    if (typeInput && institutionInput && fromInput && toInput) {
        $(this).serializeArray().map(function (data) {
            education[data.name] = data.value;
        });
        if (educations.length == 0) {
            education.id = 1;
        }
        else {
            lastEducation = educations[Object.keys(educations).sort().pop()];
            education.id = lastEducation.id + 1;
        }
        addEducation(education);
    } else {
        alert("All fields must have a valid value.");
    }

});

function addEducation(education) {
    educations.push(education);
    appendToEduTable(education);
    flashMessage(msg);
    $("#myModalEduAdd").modal({
        backdrop: 'static',
        keyboard: false  // to prevent closing with Esc button (if you want this too)
    })
}
function editEducation(id) {
    educations.forEach(function (education, i) {
        if (education.id == id) {
            $(".modal-edu-body-update").empty().append(`
                  <form id="updateEducation" action="">
                      <label for="type">Type</label>
                      <input class="form-control" type="text" name="type" value="${education.type}"/>
                      <label for="institution">institution</label>
                      <input class="form-control" type="text" name="institution" value="${education.institution}"/>
                      <label for="Form">Form</label>
                      <input class="form-control" type="date" name="from" value="${education.from}"/>
                      <label for="to">To</label>
                      <input class="form-control" type="date" name="to" value="${education.to}"/>
              `);
            $(".modal-footer").empty().append(`
                      <button type="button" type="submit" class="btn btn-primary" onClick="updateEducation(${id})">Save</button>
                  </form>
              `);
        }
    });
}
function deleteEducation(id) {
    var action = confirm("Are you sure you want to delete this education?");
    var msg = "education deleted successfully!";
    educations.forEach(function (education, i) {
        if (education.id == id && action != false) {
            educations.splice(i, 1);
            $("#education #education-" + education.id).remove();
            $("#education #buttons-" + education.id).remove();
            flashMessage(msg);
        }
    });
}
function updateEducation(id) {
    var msg = "education updated successfully!";
    flashMessage(msg);
    var education = {};
    education.id = id;
    educations.forEach(function (education, i) {
        if (education.id == id) {
            $("#updateEducation").children("input").each(function () {
                var value = $(this).val();
                var attr = $(this).attr("name");
                if (attr == "type") {
                    education.type = value;

                }
                else if (attr == "institution") {
                    education.institution = value;
                }
                else if (attr == "from") {
                    education.from = value;
                }
                else if (attr == "to") {
                    education.to = value;
                }
            });
            educations.splice(i, 1);
            educations.splice(education.id - 1, 0, education);
            $("#education #education-" + education.id).children(".educationData").each(function () {
                var attr = $(this).attr("name");
                if (attr == "type") {
                    $(this).text(education.type);
                }
                else if (attr == "institution") {
                    $(this).text(education.institution);
                }
                else if (attr == "from") {
                    $(this).text(education.from);
                }
                else if (attr == "to") {
                    $(this).text(education.to);
                }
            });
            $(".modal-edu-update").modal("toggle");

        }
    });
}
function appendToEduTable(education) {
    $("#education").append(`
        <div class="info_content mt-2 mb-2">
             <div id="education-${education.id}">
                <p class="para_heading mt-1 mb-0 educationData" name="type">${education.type}</p>
                <p class="company mt-1 mb-0 educationData" name="institution">${education.institution}</p>
                <p class="para  mt-1 mb-0 educationData" name="from" style="display: inline; padding: 0; margin: 0;">${education.from}-</p>
                <p class="para  mt-1 mb-0 educationData" name="to" style="display: inline; padding: 0; margin: 0;">${education.to}</p>
            </div>
            
            <div class="buttons" id="buttons-${education.id}" style="display: flex; flex-direction: row;">
                <button class="btn btn-primary form-control" onClick="editEducation(${education.id})" data-toggle="modal" data-target="#myModalEduUpdate")"><i class="fas fa-edit"></i></button>
                <button class="btn btn-primary form-control" onClick="deleteEducation(${education.id})"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `);
}


// THIS IS 
//         WORK EXPERIENCE LOGIC

var works = [
    {
        id: 1,
        company: "Schools",
        designation: "Modern",
        to: "2019-05-15",
        from: "2019-05-15"
    },
    {
        id: 2,
        company: "Schools",
        designation: "Don Bosco",
        to: "2019-05-15",
        from: "2019-05-15"
    }
];
$.each(works, function (i, work) {
    appendToWorkTable(work);
});
$("form").submit(function (e) {
    e.preventDefault();
});
$("form#addWork").submit(function () {
    var msg = "Work is added"
    var work = {};
    var lastWork;
    var companyInput = $('input[name="company"]').val().trim();
    var designationInput = $('input[name="designation"]').val().trim();
    var fromInput = $('input[name="from"]').val().trim();
    var toInput = $('input[name="to"]').val().trim();
    if (companyInput && designationInput && fromInput && toInput) {
        $(this).serializeArray().map(function (data) {
            work[data.name] = data.value;
        });
        if (works.length == 0) {
            work.id = 1;
        }
        else {
            lastWork = works[Object.keys(works).sort().pop()];
            work.id = lastWork.id + 1;
        }
        addWork(work);
    }
    // else {
    //     alert("All fields must have a valid value.");
    // }
});

function addWork(work) {
    works.push(work);
    appendToWorkTable(work);
    flashMessage(msg);
    $(".modal-work-create").modal("toggle");
}
function editWork(id) {
    works.forEach(function (work, i) {
        if (work.id == id) {
            $(".modal-work-body-update").empty().append(`
                  <form id="updateWork" action="">
                      <label for="company">company</label>
                      <input class="form-control" company="text" name="company" value="${work.company}"/>
                      <label for="designation">designation</label>
                      <input class="form-control" company="text" name="designation" value="${work.designation}"/>
                      <label for="Form">Form</label>
                      <input class="form-control" company="date" name="from" value="${work.from}"/>
                      <label for="to">To</label>
                      <input class="form-control" company="date" name="to" value="${work.to}"/>
              `);
            $(".modal-footer").empty().append(`
                      <button company="button" company="submit" class="btn btn-primary" onClick="updateWork(${id})">Save</button>
                  </form>
              `);
        }
    });
}
function deleteWork(id) {
    var action = confirm("Are you sure you want to delete this work?");
    var msg = "work deleted successfully!";
    works.forEach(function (work, i) {
        if (work.id == id && action != false) {
            works.splice(i, 1);
            $("#work #work-" + work.id).remove();
            $("#work #buttons-" + work.id).remove();
            flashMessage(msg);
        }
    });
}
function updateWork(id) {
    var msg = "work updated successfully!";
    flashMessage(msg);
    var work = {};
    work.id = id;
    works.forEach(function (work, i) {
        if (work.id == id) {
            $("#updateWork").children("input").each(function () {
                var value = $(this).val();
                var attr = $(this).attr("name");
                if (attr == "company") {
                    work.company = value;

                }
                else if (attr == "designation") {
                    work.designation = value;
                }
                else if (attr == "from") {
                    work.from = value;
                }
                else if (attr == "to") {
                    work.to = value;
                }
            });
            works.splice(i, 1);
            works.splice(work.id - 1, 0, work);
            $("#work #work-" + work.id).children(".workData").each(function () {
                var attr = $(this).attr("name");
                if (attr == "company") {
                    $(this).text(work.company);
                }
                else if (attr == "designation") {
                    $(this).text(work.designation);
                }
                else if (attr == "from") {
                    $(this).text(work.from);
                }
                else if (attr == "to") {
                    $(this).text(work.to);
                }
            });
            $(".modal-work-update").modal("toggle");

        }
    });
}
function appendToWorkTable(work) {
    $("#work").append(`
        <div class="info_content mt-2 mb-2">
             <div id="work-${work.id}">
                <p class="para_heading mt-1 mb-0 workData" name="company">${work.company}</p>
                <p class="company mt-1 mb-0 workData" name="designation">${work.designation}</p>
                <p class="para  mt-1 mb-0 workData" name="from" style="display: inline; padding: 0; margin: 0;">${work.from}-</p>
                <p class="para  mt-1 mb-0 workData" name="to" style="display: inline; padding: 0; margin: 0;">${work.to}</p>
            </div>
            
            <div class="buttons" id="buttons-${work.id}" style="display: flex; flex-direction: row;">
                <button class="btn btn-primary form-control" onClick="editWork(${work.id})" data-toggle="modal" data-target="#myModalWorkUpdate")"><i class="fas fa-edit"></i></button>
                <button class="btn btn-primary form-control" onClick="deleteWork(${work.id})"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `);
}



// THIS IS 
//         ACCOMPLISHMENT LOGIC





var accoms = [
    {
        id: 1,
        accomplishment: "Killed Laden",
    },
    {
        id: 2,
        accomplishment: "Build Saden",
    }
];
$.each(accoms, function (i, accom) {
    appendToAccomTable(accom);
});
$("form").submit(function (e) {
    e.preventDefault();
});
$("form#addAccom").submit(function () {
    msg = "accomplishment is added"
    var accom = {};
    var lastAccom;
    var accomplishmentInput = $('input[name="accomplishment"]').val().trim();
    if (accomplishmentInput) {
        $(this).serializeArray().map(function (data) {
            accom[data.name] = data.value;
        });
        if (accoms.length == 0) {
            accom.id = 1;
        }
        else {
            lastAccom = accoms[Object.keys(accoms).sort().pop()];
            accom.id = lastAccom.id + 1;
        }
        addAccom(accom);
    }
});

function addAccom(accom) {
    accoms.push(accom);
    flashMessage(msg);
    appendToAccomTable(accom);
    $(".modal-accom-create").modal("toggle");
}
function editAccom(id) {
    accoms.forEach(function (accom, i) {
        if (accom.id == id) {
            $(".modal-accom-body-update").empty().append(`
                  <form id="updateAccom" action="">
                      <label for="accomplishment">accomplishment</label>
                      <input class="form-control" accomplishment="text" name="accomplishment" value="${accom.accomplishment}"/>
              `);
            $(".modal-footer").empty().append(`
                      <button accomplishment="button" accomplishment="submit" class="btn btn-primary" onClick="updateAccom(${id})">Save</button>
                  </form>
              `);
        }
    });
}
function deleteAccom(id) {
    var action = confirm("Are you sure you want to delete this accom?");
    var msg = "accom deleted successfully!";
    accoms.forEach(function (accom, i) {
        if (accom.id == id && action != false) {
            accoms.splice(i, 1);
            $("#accom #accom-" + accom.id).remove();
            $("#accom #buttons-" + accom.id).remove();
            flashMessage(msg)
        }
    });
}
function updateAccom(id) {
    var msg = "accomplishment updated successfully!";
    flashMessage(msg);
    var accom = {};
    accom.id = id;
    accoms.forEach(function (accom, i) {
        if (accom.id == id) {
            $("#updateAccom").children("input").each(function () {
                var value = $(this).val();
                var attr = $(this).attr("name");
                if (attr == "accomplishment") {
                    accom.accomplishment = value;

                }
            });
            accoms.splice(i, 1);
            accoms.splice(accom.id - 1, 0, accom);
            $("#accom #accom-" + accom.id).children(".accomData").each(function () {
                var attr = $(this).attr("name");
                if (attr == "accomplishment") {
                    $(this).text(accom.accomplishment);
                }
            });
            $(".modal-accom-update").modal("toggle");

        }
    });
}
function appendToAccomTable(accom) {
    $("#accom").append(`
        <div class="info_content mt-2 mb-2">
             <div id="accom-${accom.id}">
                <p class="mt-1 mb-0 accomData" name="accomplishment">${accom.accomplishment}</p>
            </div>
            
            <div class="buttons" id="buttons-${accom.id}" style="display: flex; flex-direction: row;">
                <button class="btn btn-primary form-control" onClick="editAccom(${accom.id})" data-toggle="modal" data-target="#myModalAccomUpdate")"><i class="fas fa-edit"></i></button>
                <button class="btn btn-primary form-control" onClick="deleteAccom(${accom.id})"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `);
}


// THIS IS 
//         ACCOMPLISHMENT LOGIC


var skills = [
    {
        id: 1,
        skillLearnt: "Gun Fight",
    },
    {
        id: 2,
        skillLearnt: "Grenade Throwing",
    }
];
$.each(skills, function (i, skill) {
    appendToSkillTable(skill);
});
$("form").submit(function (e) {
    e.preventDefault();
});
$("form#addSkill").submit(function () {
    msg = "skill is added"
    var skill = {};
    var lastSkiil;
    var skillInput = $('input[name="skillLearnt"]').val().trim();
    if (skillInput) {
        $(this).serializeArray().map(function (data) {
            skill[data.name] = data.value;
        });
        if (skills.length == 0) {
            skill.id = 1;
        }
        else {
            lastSkiil = skills[Object.keys(skills).sort().pop()];
            skill.id = lastSkiil.id + 1;
        }
        addSkill(skill);
    }
});

function addSkill(skill) {
    skills.push(skill);
    appendToSkillTable(skill);
    flashMessage(msg)
    $(".modal-skill-create").modal("toggle");
}
function editSkill(id) {
    skills.forEach(function (skill, i) {
        if (skill.id == id) {
            $(".modal-skill-body-update").empty().append(`
                  <form id="updateSkill" action="">
                      <label for="skillLearnt">skill</label>
                      <input class="form-control" type="text" name="skillLearnt" value="${skill.skillLearnt}"/>
              `);
            $(".modal-footer").empty().append(`
                      <button type="button" skillLearnt="submit" class="btn btn-primary" onClick="updateSkill(${id})">Save</button>
                  </form>
              `);
        }
    });
}

function flashMessage(msg) {
    $(".alert-success").remove();
    $("#rowFlashMsg").append(`
        <div class="flash col-lg-10 alert alert-success alert-dismissible fade show" role="alert">
         ${msg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `);
}
function deleteSkill(id) {
    var action = confirm("Are you sure you want to delete this skill?");
    var msg = "skill deleted successfully!";
    skills.forEach(function (skill, i) {
        if (skill.id == id && action != false) {
            skills.splice(i, 1);
            $("#skill #skill-" + skill.id).remove();
            $("#skill #buttons-" + skill.id).remove();
            flashMessage(msg);
        }
    });
}
function updateSkill(id) {
    var msg = "skill updated successfully!";
    flashMessage(msg);
    var skill = {};
    skill.id = id;
    skills.forEach(function (skill, i) {
        if (skill.id == id) {
            $("#updateSkill").children("input").each(function () {
                var value = $(this).val();
                var attr = $(this).attr("name");
                if (attr == "skillLearnt") {
                    skill.skillLearnt = value;

                }
            });
            skills.splice(i, 1);
            skills.splice(skill.id - 1, 0, skill);
            $("#skill #skill-" + skill.id).children(".skillData").each(function () {
                var attr = $(this).attr("name");
                if (attr == "skillLearnt") {
                    $(this).text(skill.skillLearnt);
                }
            });
            $(".modal-skill-update").modal("toggle");
            flashMessage(msg)
        }
    });
}
function appendToSkillTable(skill) {
    $("#skill").append(`
        <div class="info_content mt-2 mb-2">
             <div id="skill-${skill.id}">
                <p class=" mt-1 mb-0 skillData" name="skillLearnt">${skill.skillLearnt}</p>
            </div>
            
            <div class="buttons" id="buttons-${skill.id}" style="display: flex; flex-direction: row;">
                <button class="btn btn-primary form-control" onClick="editSkill(${skill.id})" data-toggle="modal" data-target="#myModalSkillUpdate")"><i class="fas fa-edit"></i></button>
                <button class="btn btn-primary form-control" onClick="deleteSkill(${skill.id})"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `);
}









// THIS IS 
//         BIO LOGIC
var bios = [
    // {
    //     id: 1,
    //     biography: "Gun Fight",
    // }
];
$.each(bios, function (i, bio) {
    appendToBioTable(bio);
});
$("form").submit(function (e) {
    e.preventDefault();
});
$("form#addBio").submit(function () {
    msg = "bio hasbeen added"
    var bio = {};
    var lastBio;
    var bioInput = $('input[name="biography"]').val().trim();
    if (bioInput) {
        $(this).serializeArray().map(function (data) {
            bio[data.name] = data.value;
        });
        if (bios.length == 0) {
            bio.id = 1;
        }
        // else {
        //     lastBio = bios[Object.keys(bios).sort().pop()];
        //     bio.id = lastBio.id + 1;
        // }

        addBio(bio);

    }
});

function addBio(bio) {
    if (bios.length === 0) {
        bios.push(bio);
        appendToBioTable(bio);
        flashMessage(msg)
    }

    $(".modal-bio-create").modal("toggle");
}
function editBio(id) {
    bios.forEach(function (bio, i) {
        if (bio.id == id) {
            $(".modal-bio-body-update").empty().append(`
                  <form id="updateBio" action="">
                      <label for="biography">bio</label>
                      <input class="form-control" type="text" name="biography" value="${bio.biography}"/>
              `);
            $(".modal-footer").empty().append(`
                      <button type="button" biography="submit" class="btn btn-primary" onClick="updateBio(${id})">Save</button>
                  </form>
              `);
        }
    });
}
function deleteBio(id) {
    var action = confirm("Are you sure you want to delete this bio?");
    var msg = "bio deleted successfully!";
    bios.forEach(function (bio, i) {
        if (bio.id == id && action != false) {
            bios.splice(i, 1);
            $("#bio #bio-" + bio.id).remove();
            $("#bio #buttons-" + bio.id).remove();
        }
    });
}
function updateBio(id) {
    var msg = "bio updated successfully!";
    flashMessage(msg);
    var bio = {};
    bio.id = id;
    bios.forEach(function (bio, i) {
        if (bio.id == id) {
            $("#updateBio").children("input").each(function () {
                var value = $(this).val();
                var attr = $(this).attr("name");
                if (attr == "biography") {
                    bio.biography = value;

                }
            });
            bios.splice(i, 1);
            bios.splice(bio.id - 1, 0, bio);
            $("#bio #bio-" + bio.id).children(".bioData").each(function () {
                var attr = $(this).attr("name");
                if (attr == "biography") {
                    $(this).text(bio.biography);
                }
            });
            $(".modal-bio-update").modal("toggle");
        }
    });
}
function appendToBioTable(bio) {
    $("#bio").append(`
        <div class="info_content mt-2 mb-2">
             <div id="bio-${bio.id}">
                <p class="mt-1 mb-0 bioData" name="biography">${bio.biography}</p>
            </div>
            
            <div class="buttons" id="buttons-${bio.id}" style="display: flex; flex-direction: row;">
                <button class="btn btn-primary form-control" onClick="editBio(${bio.id})" data-toggle="modal" data-target="#myModalBioUpdate")"><i class="fas fa-edit"></i></button>
                <button class="btn btn-primary form-control" onClick="deleteBio(${bio.id})"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `);
}


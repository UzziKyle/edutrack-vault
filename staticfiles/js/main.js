// Nav Functionality
const menuOpen = document.querySelector('.menu-open')
const menuClose = document.querySelector('.menu-close')
const body = document.body

function menuToggle () {
    menuOpen.classList.toggle('menu-is-open')
    body.classList.toggle('menu-is-open')
}

menuOpen.addEventListener('click', menuToggle)
menuClose.addEventListener('click', menuToggle)


// Modal Functionality
const createFolderBtn = document.querySelector('.create-folder')
const uploadFileBtn = document.querySelector('.upload-file')

const folderFormOverlay = document.querySelector('.form-container.folder-form')
const fileFormOverlay = document.querySelector('.form-container.file-form')

function folderFormModalToggle() {
   folderFormOverlay.classList.toggle('is-open')
}

function fileFormModalToggle() {
   fileFormOverlay.classList.toggle('is-open')
}

if (createFolderBtn) {
    createFolderBtn.addEventListener('click', folderFormModalToggle)
}

if (uploadFileBtn) {
    uploadFileBtn.addEventListener('click', fileFormModalToggle)
}

if (folderFormOverlay) {
    folderFormOverlay.addEventListener('click', e => {
        if (!e.target.closest('form')) {
            folderFormOverlay.classList.remove('is-open')
        }
    })
}

if (fileFormOverlay) {
    fileFormOverlay.addEventListener('click', e => {
        if (!e.target.closest('form')) {
            fileFormOverlay.classList.remove('is-open')
        }
    })
}


// Item Actions
const items = document.querySelectorAll('.item')


function hideAllActions(items) {
    items.forEach(item => {
        var actions = item.querySelector('.actions')
        actions.classList.add('hidden')
    })
}


function removeIsClicked(items) {
    items.forEach(item => {
        var isClicked = item.querySelector('.is-clicked')
        if (isClicked) {
            isClicked.classList.remove('is-clicked')
        }
    })
}


items.forEach(item => {
    var openActions = item.querySelector('.open-actions')

    openActions.addEventListener('click', e => {
        var actions = item.querySelector('.actions')
        if (e.currentTarget.classList.contains('is-clicked')) {
            e.currentTarget.classList.remove('is-clicked')
            actions.classList.add('hidden')
            return
        }
        removeIsClicked(items)
        e.currentTarget.classList.add('is-clicked')
        hideAllActions(items)
        actions.classList.remove('hidden')
    })
})


body.addEventListener('click', e => {
    if (!e.target.closest('.open-actions')) {
        hideAllActions(items)
        removeIsClicked(items)
    }
})

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

createFolderBtn.addEventListener('click', folderFormModalToggle)

if (uploadFileBtn != null) {
    uploadFileBtn.addEventListener('click', fileFormModalToggle)
}

folderFormOverlay.addEventListener('click', e => {
    console.log('Twas clicked!')
    if (!e.target.closest('form')) {
        folderFormOverlay.classList.remove('is-open')
    }
})

if (fileFormOverlay != null) {
    fileFormOverlay.addEventListener('click', e => {
        if (!e.target.closest('form')) {
            fileFormOverlay.classList.remove('is-open')
        }
    })
}

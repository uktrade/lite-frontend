pipeline
        {
          agent {
             node {
                label env.CI_SLAVE
             }
          }
            parameters
            {
                // Define DRIVER parameter for running the test
                choice(name: 'DRIVER', description: 'Choose browser', choices: 'chrome\nfirefox\nheadless')

                // Define test path to run
                string(name: 'TESTS_TO_RUN', defaultValue: 'tests/test_sample.py', description: 'choose test to run')                // Define test path to run

                // Define environment to run tests on
                choice(name: 'ENVIRONMENT', description: 'choose what environment to run in', choices: 'dev\nstaging\nuat')
            }

            options
            {
                // keep last 100 builds
                buildDiscarder(logRotator(numToKeepStr: '100'))

                // add timestamp
                timestamps()
            }

            // agent any // run the pipeline on any available node
            stages
            {
                stage('SCM: code update')
                {
                    steps
                    {
                        // checking out repository
                        checkout([
                                $class: 'GitSCM', branches: [[name: 'e2e']],
                                userRemoteConfigs: [[url: 'https://github.com/uktrade/lite-internal-frontend.git']]
                        ])

                        // Create Allure report folders and grant relevant permissions
                        sh "mkdir -p ./automation_ui_tests/allure-results"
                        // sh "rm -rf ./automation_ui_tests/allure-results/*"
                        // sh "chown jenkins:jenkins ./automation_ui_tests/allure-results"
                    }
                }
                stage('Docker build')
                {
                    steps
                    {
                        script
                        {
                            sh "sudo find . -name '*.pyc' -delete"
                            // copying and building selenium base
                            sh "cp selenium-base-image/Dockerfile ."
                            docker.build("exporter/selenium_base")

                            // copying and building selenium image
                            sh "cp selenium-automation-run/Dockerfile ."
                            docker.build("exporter/selenium_image")
                        }
                    }
                }
                stage('Run test')
                {
                    steps
                    {
                        script
                        {
                            try
                            {
                                // creating timestamp
                                def now = new Date()
                                tstamp = now.format("yyyyMMdd-HH:mm:ss.SSSS", TimeZone.getTimeZone('UTC'))

                                // running selenium tests using pytest via docker
                                sh "docker run " +
                                        "--privileged " +                           // The --privileged flag gives all capabilities to the container,
                                        "--shm-size=1g " +                          // shared memory size is set to 1G to prevent chromedriver memory leak
                                        "--rm " +                                   // remove container at the end of the session
                                        "-e PYTHONPATH=/code/ " +                   // environment variable support
                                        "-w=/code " +                               // setting working directory
                                        "-v `pwd`/automation_ui_tests:/code " +                 // mount git repository to the container
                                        "exporter/selenium_image:latest " +         // the specific image that being used (latest image by default)
                                        "-v " +                                     // verbose (for debugging purpose)
                                        "${params.TESTS_TO_RUN}"
                            }
                            catch (error)
                            {
                                echo error.message
                            }
                        }
                    }
                }
            }
            post
            {
                always
                {
                    // Generate Allure Report
                    generateAllureReport()
                }
            }
        }

// Generate Allure report function
def generateAllureReport()
    {
        try
        {
            allure([
                    commandline      : '2.5.0',
                    includeProperties: false,
                    jdk              : '',
                    properties       : [[key: 'allure.tests.management.pattern', value: 'http://tms.company.com/%s']],
                    reportBuildPolicy: 'ALWAYS',
                    results          : [[path: 'automation_ui_tests/allure-results']]
            ])
        }
        catch (error)
        {
            error.message
        }
    }

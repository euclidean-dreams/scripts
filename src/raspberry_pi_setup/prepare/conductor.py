from raspberry_pi_setup.config import PI_IP_ADDRESS
from raspberry_pi_setup.pi_client import PiClient
from raspberry_pi_setup.prepare.shared import general_preparation, install_zmq, install_spdlog


def main():
    general_preparation()
    install_zmq()
    install_spdlog()

    with PiClient(PI_IP_ADDRESS) as pi:
        # portaudio
        pi.execute("sudo apt -y install libasound-dev")
        pi.execute("sudo sed -i'' -e '/^pcm\\.rear cards\\.pcm\\.rear$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.center_lfe cards\\.pcm\\.center_lfe$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.side cards\\.pcm\\.side$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.hdmi cards\\.pcm\\.hdmi$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.modem cards\\.pcm\\.modem$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.phoneline cards\\.pcm\\.phoneline$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.hdmi cards\\.pcm\\.hdmi$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.front cards\\.pcm\\.front$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround cards\\.pcm\\.surround21$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround21 cards\\.pcm\\.surround21$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround40 cards\\.pcm\\.surround40$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround41 cards\\.pcm\\.surround41$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround50 cards\\.pcm\\.surround50$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround51 cards\\.pcm\\.surround51$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.surround71 cards\\.pcm\\.surround71$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.iec958 cards\\.pcm\\.iec958$/d' /usr/share/alsa/alsa.conf")
        pi.execute("sudo sed -i'' -e '/^pcm\\.spdif iec958$/d' /usr/share/alsa/alsa.conf")
        pi.execute("curl -L -o portaudio.tgz http://files.portaudio.com/archives/pa_snapshot.tgz")
        pi.execute("tar -xzf ~/portaudio.tgz -C ~")
        pi.execute("rm ~/portaudio.tgz")
        pi.execute("cd ~/portaudio && ./configure")
        pi.execute("cd ~/portaudio && sudo make install")

        # aubio
        pi.execute("sudo apt -y install libfftw3-dev libblas-dev")
        pi.execute("curl -L -o aubio.tar.bz2 https://aubio.org/pub/aubio-0.4.9.tar.bz2")
        pi.execute("tar -xf ~/aubio.tar.bz2 -C ~")
        pi.execute("rm ~/aubio.tar.bz2")
        pi.execute("cd ~/aubio-0.4.9 && sudo ./waf configure build install --enable-fftw3 --enable-blas")

        # finalize
        pi.execute("sudo ldconfig")


if __name__ == "__main__":
    main()
